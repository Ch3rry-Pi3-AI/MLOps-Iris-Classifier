"""
pipeline_run.py
---------------
Orchestrates the sequential execution of the MLOps Iris Classifier pipeline.

Workflow
--------
1. Run the DataProcessing stage to:
   - Load the raw Iris dataset
   - Handle outliers
   - Split into train/test sets
   - Save processed artefacts to `artifacts/processed/`

2. Run the ModelTraining stage to:
   - Load processed datasets
   - Train a Decision Tree classifier
   - Evaluate metrics
   - Save the trained model and confusion matrix to `artifacts/models/`
"""

# -------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------
from src.data_processing import DataProcessing
from src.model_training import ModelTraining


# -------------------------------------------------------------------
# Pipeline Execution
# -------------------------------------------------------------------
if __name__ == "__main__":
    # Step 1: Data preparation
    data_processor = DataProcessing("artifacts/raw/data.csv")
    data_processor.run()

    # Step 2: Model training and evaluation
    trainer = ModelTraining()
    trainer.run()