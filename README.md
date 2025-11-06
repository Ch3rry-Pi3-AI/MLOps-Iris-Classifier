# 🌸 **Data Preparation — MLOps Iris Classifier**

This branch builds upon the **initial setup** by introducing the **`data_processing.py`** module inside `src/`.
It marks the **first executable workflow stage** of the **MLOps Iris Classifier** pipeline — responsible for loading the Iris dataset, handling outliers, splitting into train/test, and persisting processed artefacts.

## 🧩 **Overview**

The `DataProcessing` class implements a **reproducible preprocessing pipeline** with integrated logging and exception handling.
It produces clean, split datasets ready for model training.

### 🔍 Core Responsibilities

| Stage | Operation           | Description                                                                  |
| ----: | ------------------- | ---------------------------------------------------------------------------- |
|   1️⃣ | **Load Data**       | Reads input CSV from `artifacts/raw/data.csv`.                               |
|   2️⃣ | **Handle Outliers** | Applies the 1.5 × IQR rule to `SepalWidthCm`; replaces outliers with median. |
|   3️⃣ | **Split Data**      | Creates 80/20 train/test splits for features and target (`Species`).         |
|   4️⃣ | **Save Artefacts**  | Writes `X_train.pkl`, `X_test.pkl`, `y_train.pkl`, `y_test.pkl` to disk.     |

## 🗂️ **Updated Project Structure**

```text
mlops_iris_classifier/
├── .venv/                          # 🧩 Local virtual environment (created by uv)
├── artifacts/
│   ├── raw/
│   │   └── data.csv                # 🌸 Input Iris dataset
│   └── processed/                  # 💾 Output directory for processed data
│       ├── X_train.pkl
│       ├── X_test.pkl
│       ├── y_train.pkl
│       └── y_test.pkl
├── mlops_iris_classifier.egg-info/ # 📦 Package metadata (auto-generated)
├── pipeline/                       # ⚙️ Pipeline orchestration (future stage)
├── src/
│   ├── __init__.py
│   ├── custom_exception.py         # Unified and detailed exception handling
│   ├── logger.py                   # Centralised logging configuration
│   └── data_processing.py          # 🌸 End-to-end Iris data preparation
├── static/                         # 🌐 Visual assets (optional)
├── templates/                      # 🧩 Placeholder for web/API templates
├── .gitignore                      # 🚫 Git ignore rules
├── .python-version                 # 🐍 Python version pin
├── pyproject.toml                  # ⚙️ Project metadata and uv configuration
├── requirements.txt                # 📦 Python dependencies
├── setup.py                        # 🔧 Editable install support
└── uv.lock                         # 🔒 Locked dependency versions
```

## ⚙️ **How to Run the Data Processing Module**

After activating the virtual environment and ensuring your dataset is located at `artifacts/raw/data.csv`, run:

```bash
python src/data_processing.py
```

### ✅ **Expected Successful Output**

```console
2025-11-06 23:10:06,743 - INFO - Data read successfully. Shape: (150, 6)
2025-11-06 23:10:06,744 - INFO - Starting outlier handling for column: SepalWidthCm
2025-11-06 23:10:06,747 - INFO - Outliers handled successfully for column: SepalWidthCm
2025-11-06 23:10:06,749 - INFO - Data split successfully into train/test.
2025-11-06 23:10:06,755 - INFO - Processed files saved successfully for data-processing step.
```

This confirms that:

* The data was read successfully.
* Outliers were detected and replaced using the IQR rule.
* Train/test splits were created and saved under `artifacts/processed/`.

## 🧠 **Implementation Highlights**

* **Integrated Logging** via `src/logger.py`
  Every major step produces timestamped logs for full traceability.

* **Unified Exception Handling** via `src/custom_exception.py`
  Failures are raised with consistent, contextual messages for quicker debugging.

* **Minimal, Modular Design**
  The `DataProcessing` class is importable and ready for integration with future stages (training, evaluation, pipelines).

## 🧩 **Integration Guidelines**

| File                      | Purpose                                                   |
| ------------------------- | --------------------------------------------------------- |
| `src/data_processing.py`  | Executes the Iris preprocessing workflow end-to-end.      |
| `src/custom_exception.py` | Provides consistent, traceable error reporting.           |
| `src/logger.py`           | Ensures structured, timestamped logs for reproducibility. |

✅ **In summary:**
This branch converts the repository from a static scaffold into a **functional preprocessing stage** for the Iris classifier — with reproducible outputs, consistent logging, and robust error handling.
Run it with `python src/data_processing.py` to generate training-ready artefacts for the next steps in the MLOps pipeline.
