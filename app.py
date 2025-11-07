"""
app.py
======
Flask web app for Iris species prediction.

Features
--------
- Loads trained model from artifacts/models/model.pkl
- Validates numeric inputs against sensible Iris ranges
- Shows helpful stats (Range, Mean, IQR) above inputs
- Wider form container, full-width Predict button
- Subtle background image overlay (~20% opacity)
"""

from __future__ import annotations

from typing import Any, Dict

import joblib
import numpy as np
from flask import Flask, render_template, request

# Optional integration with project logger / exceptions
try:
    from src.logger import get_logger
    from src.custom_exception import CustomException

    logger = get_logger(__name__)
except Exception:
    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    class CustomException(Exception):
        """Fallback CustomException if src modules not yet available."""
        pass


# -------------------------------------------------------------------
# App & Model
# -------------------------------------------------------------------
app = Flask(__name__)

MODEL_PATH = "artifacts/models/model.pkl"
model = joblib.load(MODEL_PATH)
logger.info("Model loaded from %s", MODEL_PATH)


# -------------------------------------------------------------------
# UI Config (Iris stats from the canonical dataset)
# All values in centimetres. Steps chosen for smooth arrow-key increments.
# -------------------------------------------------------------------
IRIS_FEATURES: Dict[str, Dict[str, Any]] = {
    "SepalLengthCm": {
        "label": "Sepal Length (cm)",
        "min": 4.3, "max": 7.9, "step": 0.1,
        "mean": 5.84, "iqr": (5.10, 6.40),
        "suggested": [5.1, 5.8, 6.4],
    },
    "SepalWidthCm": {
        "label": "Sepal Width (cm)",
        "min": 2.0, "max": 4.4, "step": 0.1,
        "mean": 3.05, "iqr": (2.80, 3.30),
        "suggested": [2.8, 3.0, 3.3],
    },
    "PetalLengthCm": {
        "label": "Petal Length (cm)",
        "min": 1.0, "max": 6.9, "step": 0.1,
        "mean": 3.76, "iqr": (1.60, 5.10),
        "suggested": [1.6, 3.8, 5.1],
    },
    "PetalWidthCm": {
        "label": "Petal Width (cm)",
        "min": 0.1, "max": 2.5, "step": 0.1,
        "mean": 1.20, "iqr": (0.30, 1.80),
        "suggested": [0.3, 1.2, 1.8],
    },
}

# Defaults (means make a sensible starting point)
DEFAULTS = {k: v["mean"] for k, v in IRIS_FEATURES.items()}


def _parse_and_validate(name: str, value: str) -> float:
    """
    Convert posted value to float and validate it against configured min/max.

    Parameters
    ----------
    name : str
        Feature key from IRIS_FEATURES.
    value : str
        Posted value to parse.

    Returns
    -------
    float
        Parsed and validated value.

    Raises
    ------
    CustomException
        If parsing fails or value is out of range.
    """
    conf = IRIS_FEATURES[name]

    # Convert to float
    try:
        x = float(value)
    except Exception as e:
        raise CustomException(f"{conf['label']}: value must be numeric.") from e

    # Range validation (disallows negatives automatically via min)
    if x < conf["min"] or x > conf["max"]:
        raise CustomException(
            f"{conf['label']}: {x} is out of range "
            f"[{conf['min']}, {conf['max']}]."
        )

    return x


# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    error = None

    # Persist user inputs on page state
    inputs = DEFAULTS.copy()

    if request.method == "POST":
        try:
            sl = _parse_and_validate("SepalLengthCm", request.form.get("SepalLengthCm", ""))
            sw = _parse_and_validate("SepalWidthCm", request.form.get("SepalWidthCm", ""))
            pl = _parse_and_validate("PetalLengthCm", request.form.get("PetalLengthCm", ""))
            pw = _parse_and_validate("PetalWidthCm", request.form.get("PetalWidthCm", ""))

            inputs = {
                "SepalLengthCm": sl,
                "SepalWidthCm": sw,
                "PetalLengthCm": pl,
                "PetalWidthCm": pw,
            }

            data = np.array([[sl, sw, pl, pw]])
            prediction = model.predict(data)[0]
            logger.info("Prediction successful: %s", str(prediction))

        except Exception as e:
            error = str(e)
            logger.error("Prediction failed: %s", error)

    return render_template(
        "index.html",
        prediction=prediction,
        error=error,
        features=IRIS_FEATURES,
        inputs=inputs,
    )


# -------------------------------------------------------------------
# Entrypoint
# -------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
