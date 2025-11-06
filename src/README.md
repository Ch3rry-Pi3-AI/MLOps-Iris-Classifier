# `src/` README — Core Utilities (Custom Exception & Logger)

This folder contains **foundational utilities** for the **Iris Classifier MLOps pipeline**.
These modules provide **consistent logging** and **structured error handling** across all workflow stages — including **data ingestion**, **preprocessing**, **model training**, **evaluation**, and **deployment**.

## 📁 Folder Overview

```text
src/
├─ custom_exception.py   # Unified and detailed exception handling
└─ logger.py             # Centralised logging configuration
```

## ⚠️ `custom_exception.py` — Unified Error Handling

### Purpose

Defines a **CustomException** class that captures detailed debugging context for any error that occurs in the pipeline — whether during **CSV ingestion**, **feature standardisation**, **model fitting**, or **API inference**.

### Key Features

* Captures the **file name** and **line number** where the exception occurred
* Includes a formatted **traceback** for quick and consistent debugging
* Works with flexible inputs:

  * the `sys` module,
  * an explicit exception instance, or
  * no arguments (defaults to the current exception via `sys.exc_info()`)

### Example Usage

```python
from src.custom_exception import CustomException
import sys
import pandas as pd

try:
    df = pd.read_csv("data/raw/iris.csv")
    if df.empty:
        raise ValueError("Iris dataset is empty.")
except Exception as e:
    raise CustomException("Error during data ingestion", sys) from e
```

### Output Example

```
Error in /mlops-iris-classifier/src/data_ingestion.py, line 24: Error during data ingestion
Traceback (most recent call last):
  File "/mlops-iris-classifier/src/data_ingestion.py", line 24, in <module>
    df = pd.read_csv("data/raw/iris.csv")
ValueError: Iris dataset is empty.
```

This ensures all exceptions are reported in a **consistent, traceable format** across the Iris pipeline — from data preparation to inference.

## 🪵 `logger.py` — Centralised Logging

### Purpose

Provides a **standardised logging setup** for the Iris project.
Each log message is timestamped and written to a dated log file inside a `logs/` directory — enabling a clear audit trail across **data transformations**, **training runs**, and **inference requests**.

### Log File Format

* Directory: `logs/`
* File name: `log_YYYY-MM-DD.log`
* Example: `logs/log_2025-11-06.log`

### Default Configuration

* Logging level: `INFO`
* Format:

  ```
  %(asctime)s - %(levelname)s - %(message)s
  ```

### Example Usage

```python
from src.logger import get_logger

logger = get_logger(__name__)

logger.info("Starting Iris classification pipeline.")
logger.warning("Missing values detected in 'sepal_length'. Applying mean imputation.")
logger.error("Model training aborted due to invalid class labels.")
```

### Output Example

```
2025-11-06 12:04:31,892 - INFO - Starting Iris classification pipeline.
2025-11-06 12:04:32,441 - WARNING - Missing values detected in 'sepal_length'. Applying mean imputation.
2025-11-06 12:04:33,009 - ERROR - Model training aborted due to invalid class labels.
```

## 🧩 Integration Guidelines

| Module Type        | Use `CustomException` for…                            | Use `get_logger` for…                                             |
| ------------------ | ----------------------------------------------------- | ----------------------------------------------------------------- |
| Data Ingestion     | File loading failures, schema mismatches, empty files | File paths, record counts, schema summaries                       |
| Preprocessing      | Type conversion or encoding errors                    | Feature scaling, imputations, column transformations              |
| Model Training     | Invalid targets, convergence issues, NaNs in features | Hyperparameters, metrics per epoch, validation loss tracking      |
| Evaluation         | Metric computation, output file issues                | Fold-level accuracy, confusion matrix, classification report logs |
| Inference/Serving  | Invalid payloads, missing model artefacts             | Request summaries, model version, confidence scores               |
| CI/CD & Scheduling | Failed task steps, API timeouts                       | Pipeline stage logs, run durations, job retries                   |

**Tip:** Combine both tools for robust debugging and traceability:

```python
from src.logger import get_logger
from src.custom_exception import CustomException
import sys

logger = get_logger(__name__)

def classify(model, X):
    try:
        logger.info(f"Inference started for {len(X)} samples.")
        predictions = model.predict(X)
        logger.info("Inference completed successfully.")
        return predictions
    except Exception as e:
        logger.error("Inference step failed.")
        raise CustomException("Iris classification inference error", sys) from e
```

## ✅ In summary

* `custom_exception.py` provides **clear, contextual error messages** for every exception.
* `logger.py` enables **structured, timestamped logging** across all project modules.

Together they form the **core reliability backbone** of the **MLOps Iris Classifier** pipeline — supporting reproducibility, debugging, and transparent experiment tracking throughout the lifecycle.
