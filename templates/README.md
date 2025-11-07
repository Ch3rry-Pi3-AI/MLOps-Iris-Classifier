# 🧩 **`templates/` Folder — Flask HTML Templates**

The `templates/` directory contains all **HTML templates** used by the **Flask-based Iris Species Prediction App**.
These files define the **structure**, **layout**, and **interactive elements** of the web interface that connects the user to the trained MLOps Iris Classifier model.

## 📁 **Folder Overview**

```text
templates/
└─ index.html     # 🧠 Main web page for user input and prediction display
```

## 🧠 **Purpose**

Flask automatically looks inside the `templates/` directory when rendering web pages using the `render_template()` function.
This folder provides a structured, responsive, and user-friendly interface that allows users to interact with the trained model directly from their browser.

| File         | Description                                                                                                                            |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| `index.html` | Primary user interface for the Iris classifier. Contains feature guidance, data entry fields, a Predict button, and a results section. |

## 🎨 **Key Design Features**

* **Feature Guidance Section** — Displays the **range**, **mean**, and **interquartile range (IQR)** for each Iris feature to help users enter realistic values.
* **Input Validation** — Each numerical input enforces sensible `min`, `max`, and `step` values based on dataset statistics.
* **Data Suggestions** — Datalists provide **example measurements** for quick selection.
* **Responsive Layout** — Uses a flexible grid system to ensure proper spacing and readability on both desktop and mobile.
* **Full-Width Predict Button** — Large, easily clickable button aligned to the container width for intuitive usability.
* **Dynamic Background** — Faint overlay image (`app_background.jpg`) injected via Flask to create a clean, subtle visual theme.

## ⚙️ **Template Logic and Integration**

This page is rendered by **`app.py`** via Flask’s `render_template()` function:

```python
from flask import Flask, render_template, request
import joblib, numpy as np

app = Flask(__name__)
model = joblib.load("artifacts/models/model.pkl")

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    # features and default inputs passed to the template
    return render_template("index.html", prediction=prediction, features=features, inputs=inputs)
```

Within `index.html`, Jinja templating is used to dynamically insert variables:

```html
<input
  type="number"
  name="SepalLengthCm"
  min="{{ features['SepalLengthCm'].min }}"
  max="{{ features['SepalLengthCm'].max }}"
  step="{{ features['SepalLengthCm'].step }}"
  value="{{ inputs['SepalLengthCm'] }}"
  required
/>
```

This allows **server-side data** (e.g., feature ranges or predictions) to populate the form automatically without hardcoding values.

## 🪄 **User Workflow**

1. The user accesses the root route (`/`) served by Flask.
2. `index.html` is rendered, displaying input fields and feature guidance.
3. The user enters measurements (within sensible limits) and clicks **Predict**.
4. The trained model (`model.pkl`) is invoked to generate a prediction.
5. The prediction result appears dynamically on the same page.

## 🧩 **Styling Integration**

`index.html` uses styles defined in `static/style.css`, referenced through Flask’s static path resolution:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
```

The background image is injected dynamically for portability:

```html
<style>
  .bg-overlay {
    background-image: url("{{ url_for('static', filename='img/app_background.jpg') }}");
  }
</style>
```

## ✅ **In Summary**

The `templates/` folder provides:

* A **dynamic HTML structure** powered by Jinja templating
* **Real-time integration** with Flask routes and model predictions
* **Responsive and user-friendly design** consistent with modern UI principles
* **Separation of concerns** — back-end logic in `app.py`, front-end structure in `index.html`

This template serves as the **presentation layer** of the Iris Species Prediction App, offering a smooth and informative experience for users exploring the MLOps pipeline in action.
