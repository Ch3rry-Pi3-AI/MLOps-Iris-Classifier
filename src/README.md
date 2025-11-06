# `src/` README — Core Utilities (Custom Exception, Logger, Data Processing & Model Training)

This folder contains **core modules** for the **Iris Classifier MLOps pipeline**.
It provides the essential components for **logging**, **error handling**, **data preparation**, and **model training**, ensuring a consistent, reproducible workflow across all stages — from ingestion and preprocessing to training, evaluation, and deployment.

## 📁 Folder Overview

```text
src/
├─ custom_exception.py   # Unified and detailed exception handling
├─ logger.py             # Centralised logging configuration
├─ data_processing.py    # Loads data, handles outliers, and splits/serialises sets
└─ model_training.py     # Trains and evaluates the Decision Tree model
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

This ensures all exceptions are reported in a **uniform and traceable** format across the pipeline — from raw data loading to inference.

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

Implements the **DataProcessing** class, responsible for preparing the Iris dataset before model training.
It loads the dataset, handles outliers, performs a train/test split, and persists processed artefacts to disk.

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
2025-11-06 14:12:11,301 - INFO - Data read successfully. Shape: (150, 6)
2025-11-06 14:12:11,402 - INFO - Starting outlier handling for column: SepalWidthCm
2025-11-06 14:12:11,506 - INFO - Outliers handled successfully for column: SepalWidthCm
2025-11-06 14:12:11,611 - INFO - Data split successfully into train/test.
2025-11-06 14:12:11,713 - INFO - Processed files saved successfully for data-processing step.
```

This module is the **entry point for preprocessing**, producing clean, ready-to-train data for the modelling pipeline.

## 🌳 `model_training.py` — Model Training and Evaluation

### Purpose

Implements the **ModelTraining** class, which performs **training and evaluation** of the Decision Tree classifier on the processed Iris data.
It loads datasets, fits the model, calculates performance metrics, and saves the model artefacts and confusion matrix.

### Workflow

| Step               | Description                                                                                 |
| ------------------ | ------------------------------------------------------------------------------------------- |
| 1️⃣ Load Data      | Loads `X_train`, `X_test`, `y_train`, and `y_test` from `artifacts/processed/`.             |
| 2️⃣ Train Model    | Trains a `DecisionTreeClassifier` with `gini` criterion and depth limit of 30.              |
| 3️⃣ Evaluate Model | Computes **accuracy**, **precision**, **recall**, and **F1-score**, logging each metric.    |
| 4️⃣ Save Artefacts | Persists `model.pkl` and saves a **confusion matrix** visualisation to `artifacts/models/`. |

### Example Usage

```python
from src.model_training import ModelTraining

if __name__ == "__main__":
    trainer = ModelTraining()
    trainer.run()
```

### Output Example

```
2025-11-06 23:25:17,312 - INFO - ModelTraining initialised successfully.
2025-11-06 23:25:17,456 - INFO - Processed data loaded successfully.
2025-11-06 23:25:17,498 - INFO - Model trained and saved successfully.
2025-11-06 23:25:17,557 - INFO - Accuracy Score  : 0.9667
2025-11-06 23:25:17,558 - INFO - Precision Score : 0.9680
2025-11-06 23:25:17,559 - INFO - Recall Score    : 0.9667
2025-11-06 23:25:17,560 - INFO - F1 Score        : 0.9666
2025-11-06 23:25:17,601 - INFO - Confusion matrix saved successfully.
```

This module represents the **training and evaluation stage** of the pipeline, completing the end-to-end workflow from raw data to a trained model.

## 🧩 Integration Guidelines

| Module Type        | Use `CustomException` for…                            | Use `get_logger` for…                                        |
| ------------------ | ----------------------------------------------------- | ------------------------------------------------------------ |
| Data Ingestion     | File loading failures, schema mismatches, empty files | File paths, record counts, schema summaries                  |
| Preprocessing      | Outlier handling, feature type errors, missing values | Feature distributions, scaling/encoding summaries            |
| Model Training     | Invalid targets, training failures, missing artefacts | Hyperparameters, metrics per epoch, validation loss tracking |
| Evaluation         | Metric computation, confusion matrix output issues    | Accuracy, F1-score, and confusion matrix summaries           |
| Inference/Serving  | Invalid payloads, missing model artefacts             | Request summaries, model version, confidence scores          |
| CI/CD & Scheduling | Failed task steps, API timeouts                       | Pipeline stage logs, run durations, job retries              |

**Tip:** Use all four modules together for robust, transparent pipeline execution:

```python
from src.data_processing import DataProcessing
from src.model_training import ModelTraining
from src.logger import get_logger
from src.custom_exception import CustomException
import sys

logger = get_logger(__name__)

try:
    processor = DataProcessing("artifacts/raw/data.csv")
    processor.run()
    trainer = ModelTraining()
    trainer.run()
    logger.info("End-to-end Iris training pipeline completed successfully.")
except Exception as e:
    logger.error("Pipeline execution failed.")
    raise CustomException("Iris pipeline execution error", sys) from e
```

## ✅ In summary

* `custom_exception.py` ensures **clear, contextual error reporting**.
* `logger.py` provides **structured, timestamped logging**.
* `data_processing.py` establishes a **reliable preprocessing workflow**.
* `model_training.py` completes the **training and evaluation stage**.

Together, these modules form the **core reliability, preprocessing, and modelling layer** of the **MLOps Iris Classifier** pipeline — ensuring maintainability, traceability, and reproducibility across all project stages.
