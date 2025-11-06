# `src/` README — Core Utilities (Custom Exception, Logger & Data Processing)

This folder contains **core modules** for the **Iris Classifier MLOps pipeline**.
It provides the building blocks for **logging**, **error handling**, and **data preparation**, ensuring a consistent, reproducible workflow across data ingestion, preprocessing, model training, evaluation, and deployment.

## 📁 Folder Overview

```text
src/
├─ custom_exception.py   # Unified and detailed exception handling
├─ logger.py             # Centralised logging configuration
└─ data_processing.py    # Loads data, handles outliers, and splits/serialises sets
```

## ⚠️ `custom_exception.py` — Unified Error Handling

### Purpose

Defines a **CustomException** class that provides detailed debugging context for any error in the pipeline — whether during **CSV ingestion**, **feature preprocessing**, **model fitting**, or **API inference**.

### Key Features

* Captures the **file name** and **line number** of the error
* Includes a formatted **traceback** for consistent debugging
* Flexible inputs:

  * the `sys` module,
  * an exception instance, or
  * nothing (defaults to `sys.exc_info()`)

### Example Usage

```python
from src.custom_exception import CustomException
import sys
import pandas as pd

try:
    df = pd.read_csv("artifacts/raw/data.csv")
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
    df = pd.read_csv("artifacts/raw/data.csv")
ValueError: Iris dataset is empty.
```

This ensures all exceptions are reported in a **uniform and traceable** format across the Iris pipeline — from raw data loading to inference.

## 🪵 `logger.py` — Centralised Logging

### Purpose

Provides a **standardised logging setup** for the Iris MLOps project. Each log entry is timestamped and stored in a dated log file within a `logs/` directory — creating a clear audit trail for **data transformations**, **training runs**, and **inference operations**.

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
logger.warning("Outliers detected in 'SepalWidthCm'. Applying median replacement.")
logger.error("Training aborted due to invalid class distribution.")
```

### Output Example

```
2025-11-06 12:04:31,892 - INFO - Starting Iris classification pipeline.
2025-11-06 12:04:32,441 - WARNING - Outliers detected in 'SepalWidthCm'. Applying median replacement.
2025-11-06 12:04:33,009 - ERROR - Training aborted due to invalid class distribution.
```

## 🌸 `data_processing.py` — Iris Dataset Preparation

### Purpose

Implements the **DataProcessing** class, responsible for preparing the Iris dataset before model training. It loads the dataset, handles outliers, performs a train/test split, and persists processed artefacts to disk.

### Workflow

| Step                | Description                                                                                                                                 |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| 1️⃣ Load Data       | Reads the Iris dataset from `artifacts/raw/data.csv`.                                                                                       |
| 2️⃣ Handle Outliers | Uses the IQR rule (1.5 × IQR) to detect outliers in `SepalWidthCm` and replaces them with the column median.                                |
| 3️⃣ Split Data      | Separates features (`SepalLengthCm`, `SepalWidthCm`, `PetalLengthCm`, `PetalWidthCm`) and target (`Species`), then performs an 80/20 split. |
| 4️⃣ Save Artefacts  | Persists `X_train`, `X_test`, `y_train`, `y_test` as `.pkl` files in `artifacts/processed/`.                                                |

### Example Usage

```python
from src.data_processing import DataProcessing

if __name__ == "__main__":
    processor = DataProcessing("artifacts/raw/data.csv")
    processor.run()
```

### Output Example

```
2025-11-06 14:12:11,301 - INFO - Data read successfully. Shape: (150, 5)
2025-11-06 14:12:11,402 - INFO - Starting outlier handling for column: SepalWidthCm
2025-11-06 14:12:11,506 - INFO - Outliers handled successfully for column: SepalWidthCm
2025-11-06 14:12:11,611 - INFO - Data split successfully into train/test.
2025-11-06 14:12:11,713 - INFO - Processed files saved successfully for data-processing step.
```

This module is the **entry point for preprocessing**, producing clean, ready-to-train data for the modelling pipeline.

## 🧩 Integration Guidelines

| Module Type        | Use `CustomException` for…                            | Use `get_logger` for…                                             |
| ------------------ | ----------------------------------------------------- | ----------------------------------------------------------------- |
| Data Ingestion     | File loading failures, schema mismatches, empty files | File paths, record counts, schema summaries                       |
| Preprocessing      | Outlier handling, feature type errors, missing values | Feature distributions, scaling/encoding summaries                 |
| Model Training     | Invalid targets, convergence issues, NaNs in features | Hyperparameters, metrics per epoch, validation loss tracking      |
| Evaluation         | Metric computation, output file issues                | Fold-level accuracy, confusion matrix, classification report logs |
| Inference/Serving  | Invalid payloads, missing model artefacts             | Request summaries, model version, confidence scores               |
| CI/CD & Scheduling | Failed task steps, API timeouts                       | Pipeline stage logs, run durations, job retries                   |

**Tip:** Use all three modules together for robust, transparent pipeline execution:

```python
from src.data_processing import DataProcessing
from src.logger import get_logger
from src.custom_exception import CustomException
import sys

logger = get_logger(__name__)

try:
    processor = DataProcessing("artifacts/raw/data.csv")
    processor.run()
    logger.info("Data preparation pipeline completed successfully.")
except Exception as e:
    logger.error("Data preparation failed.")
    raise CustomException("Iris data processing error", sys) from e
```

## ✅ In summary

* `custom_exception.py` ensures **clear, contextual error reporting**.
* `logger.py` provides **structured, timestamped logging** across modules.
* `data_processing.py` establishes a **clean, reproducible data preparation workflow**.

Together, these modules form the **core reliability and preprocessing layer** of the **MLOps Iris Classifier** pipeline — supporting maintainability, traceability, and scalability across all future development stages.
