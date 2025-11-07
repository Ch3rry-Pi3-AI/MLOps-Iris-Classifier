# ⚙️ **Training Pipeline — MLOps Iris Classifier**

This branch builds upon the **model training stage** by introducing the **`training_pipeline.py`** module inside the `pipeline/` folder.
It represents the **fourth executable workflow stage** of the **MLOps Iris Classifier** pipeline — combining all previous stages into a single, orchestrated execution flow for full automation and reproducibility.

<p align="center">
  <img src="img/flask/flask_app.png" alt="MLOps Iris Pipeline Overview" width="720"/>
</p>

## 🧩 **Overview**

The **`training_pipeline.py`** script acts as the **orchestration layer** for the MLOps workflow, executing both the **data preparation** and **model training** stages in one seamless run.
It ensures a consistent, traceable process by leveraging the modular design of `src/data_processing.py` and `src/model_training.py`, with integrated logging and exception handling.

### 🔍 Core Responsibilities

| Stage | Operation              | Description                                                                                                                                          |
| ----: | ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
|   1️⃣ | **Data Processing**    | Invokes `DataProcessing` to load the raw dataset, handle outliers, split train/test sets, and save processed artefacts under `artifacts/processed/`. |
|   2️⃣ | **Model Training**     | Calls `ModelTraining` to load processed data, train a Decision Tree model, evaluate performance, and save results under `artifacts/models/`.         |
|   3️⃣ | **Logging**            | Records each step, from ingestion to evaluation, via `src/logger.py` for full traceability.                                                          |
|   4️⃣ | **Exception Handling** | Standardises all errors through `src/custom_exception.py` for consistent debugging.                                                                  |

## 🗂️ **Updated Project Structure**

```text
mlops_iris_classifier/
├── .venv/                          # 🧩 Local virtual environment (created by uv)
├── artifacts/
│   ├── raw/
│   │   └── data.csv                # 🌸 Input Iris dataset
│   ├── processed/                  # 💾 Preprocessed artefacts (from DataProcessing)
│   │   ├── X_train.pkl
│   │   ├── X_test.pkl
│   │   ├── y_train.pkl
│   │   └── y_test.pkl
│   └── models/                     # 🧠 Trained model and evaluation artefacts
│       ├── model.pkl
│       └── confusion_matrix.png
├── img/
│   └── flask/
│       └── flask_app.png           # 🖼️ Pipeline overview or app preview
├── mlops_iris_classifier.egg-info/ # 📦 Package metadata (auto-generated)
├── pipeline/                       # ⚙️ Workflow orchestration layer
│   └── training_pipeline.py        # Executes data preparation + model training
├── src/
│   ├── __init__.py
│   ├── custom_exception.py         # Unified and detailed exception handling
│   ├── logger.py                   # Centralised logging configuration
│   ├── data_processing.py          # 🌱 Data preparation workflow
│   └── model_training.py           # 🌳 Model training and evaluation workflow
├── static/                         # 🎨 Visual assets (used in Flask UI)
├── templates/                      # 🧩 Flask HTML templates (for app stage)
├── .gitignore                      # 🚫 Git ignore rules
├── .python-version                 # 🐍 Python version pin
├── pyproject.toml                  # ⚙️ Project metadata and uv configuration
├── requirements.txt                # 📦 Python dependencies
├── setup.py                        # 🔧 Editable install support
└── uv.lock                         # 🔒 Locked dependency versions
```

## ⚙️ **How to Run the Training Pipeline**

After verifying your dataset exists under `artifacts/raw/data.csv`, execute the following command:

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

* Both stages executed successfully in sequence.
* Artefacts were saved in their respective directories.
* All steps were logged consistently for reproducibility.

## 🧱 **Code Overview**

```python
from src.data_processing import DataProcessing
from src.model_training import ModelTraining

if __name__ == "__main__":
    # Step 1: Data Processing
    data_processor = DataProcessing("artifacts/raw/data.csv")
    data_processor.run()

    # Step 2: Model Training
    trainer = ModelTraining()
    trainer.run()
```

This design ensures that each workflow stage is **self-contained**, yet fully interoperable when executed sequentially.

## 🧩 **Integration Summary**

| File                            | Purpose                                                      |
| ------------------------------- | ------------------------------------------------------------ |
| `pipeline/training_pipeline.py` | Coordinates the end-to-end pipeline execution.               |
| `src/data_processing.py`        | Handles data loading, cleaning, and splitting.               |
| `src/model_training.py`         | Trains and evaluates the Decision Tree model.                |
| `src/logger.py`                 | Provides structured, timestamped logging.                    |
| `src/custom_exception.py`       | Ensures clear, contextual error handling.                    |
| `artifacts/`                    | Stores all datasets, trained models, and evaluation outputs. |

## 💡 **Example Workflow**

1. Prepare and clean your data:

   ```bash
   python src/data_processing.py
   ```

2. Train and evaluate the model:

   ```bash
   python src/model_training.py
   ```

3. Or run the entire workflow automatically:

   ```bash
   python pipeline/training_pipeline.py
   ```

4. Review the generated artefacts under `artifacts/processed/` and `artifacts/models/`.

## ✅ **In Summary**

This branch elevates the **MLOps Iris Classifier** into a **fully orchestrated machine learning pipeline**, linking all stages — from raw data to trained model — in a single reproducible process.
The `training_pipeline.py` module ensures that data processing and model training execute reliably, with full logging, error handling, and artefact management.

It establishes the foundation for **future automation**, including CI/CD integration, **MLflow experiment tracking**, or **Kubeflow pipeline deployment**.