# ⚙️ **`pipeline/` Folder — Workflow Orchestration**

The `pipeline/` directory contains the **workflow automation scripts** for the **MLOps Iris Classifier** project.
This layer coordinates multiple stages of the MLOps pipeline — from data preparation to model training — ensuring a **seamless, reproducible workflow** for both development and production.

## 📁 **Folder Overview**

```text
pipeline/
└─ training_pipeline.py   # 🧩 Orchestrates the end-to-end Iris ML pipeline
```

## 🧩 **Purpose**

`training_pipeline.py` serves as the **entry point for executing the entire training workflow**.
It sequentially runs both the **data processing** and **model training** stages, maintaining proper task order, dependency management, and clear logging throughout execution.

| File                   | Description                                                                                                     |
| ---------------------- | --------------------------------------------------------------------------------------------------------------- |
| `training_pipeline.py` | Runs the complete workflow: data ingestion → preprocessing → model training → evaluation → artefact generation. |

## 🧠 **Key Responsibilities**

| Stage | Operation            | Description                                                                                                                                            |
| ----: | -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
|   1️⃣ | **Data Preparation** | Calls `DataProcessing` to load raw data, handle outliers, split train/test sets, and save processed artefacts under `artifacts/processed/`.            |
|   2️⃣ | **Model Training**   | Invokes `ModelTraining` to load processed data, train a Decision Tree model, evaluate performance metrics, and save results under `artifacts/models/`. |
|   3️⃣ | **Pipeline Logging** | Both stages automatically log events and metrics using `src/logger.py` for full traceability.                                                          |
|   4️⃣ | **Error Handling**   | Any runtime issue is caught and standardised via `src/custom_exception.py`.                                                                            |

## ⚙️ **How to Run the Training Pipeline**

After setting up your environment and ensuring the raw dataset is available under `artifacts/raw/data.csv`, run:

```bash
python pipeline/training_pipeline.py
```

### ✅ **Expected Successful Output**

```console
2025-11-07 12:45:16,210 - INFO - Data read successfully. Shape: (150, 6)
2025-11-07 12:45:16,300 - INFO - Outliers handled successfully for column: SepalWidthCm
2025-11-07 12:45:16,404 - INFO - Data split successfully into train/test sets.
2025-11-07 12:45:16,517 - INFO - Processed data saved successfully under artifacts/processed/
2025-11-07 12:45:16,621 - INFO - ModelTraining initialised successfully.
2025-11-07 12:45:16,704 - INFO - Processed data loaded successfully.
2025-11-07 12:45:16,782 - INFO - Model trained and saved successfully.
2025-11-07 12:45:16,897 - INFO - Accuracy Score  : 1.0000
2025-11-07 12:45:16,898 - INFO - Precision Score : 1.0000
2025-11-07 12:45:16,898 - INFO - Recall Score    : 1.0000
2025-11-07 12:45:16,899 - INFO - F1 Score        : 1.0000
2025-11-07 12:45:17,041 - INFO - Confusion matrix saved successfully.
```

This confirms that:

* Data preprocessing and model training completed successfully.
* Artefacts were saved to their respective directories.
* Metrics were computed and logged as expected.

## 🧱 **Code Overview**

```python
from src.data_processing import DataProcessing
from src.model_training import ModelTraining

if __name__ == "__main__":
    # Step 1: Data processing
    data_processor = DataProcessing("artifacts/raw/data.csv")
    data_processor.run()

    # Step 2: Model training
    trainer = ModelTraining()
    trainer.run()
```

This script ensures a **linear, reproducible execution flow** without requiring manual stage-by-stage runs.

## 🪄 **Integration Notes**

* The pipeline can be easily extended in future stages for **model registry integration**, **MLflow tracking**, or **Kubeflow Pipelines**.
* All artefacts produced here are versioned and logged, enabling full reproducibility across development environments.
* Designed to run locally or inside a CI/CD workflow for automated retraining.

## ✅ **In Summary**

The `pipeline/` folder acts as the **control layer** for the Iris MLOps workflow — connecting preprocessing, training, and evaluation steps into one unified execution script.
It ensures every stage of the project can be executed **reliably, traceably, and repeatably**, forming the backbone for future **pipeline automation and deployment**.