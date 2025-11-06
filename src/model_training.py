"""
model_training.py
=================
Implements the ``ModelTraining`` class for the Iris classification workflow.

Overview
--------
This module represents the **model development stage** of the MLOps Iris Classifier pipeline.
It loads preprocessed training and test datasets, trains a Decision Tree classifier,
evaluates model performance, logs key metrics, and saves both the trained model
and confusion matrix visualisation to disk.

Responsibilities
----------------
1. Load processed feature and target datasets.
2. Train a Decision Tree model with predefined hyperparameters.
3. Evaluate model performance (accuracy, precision, recall, F1-score).
4. Generate and save a confusion matrix plot.
5. Persist the trained model to ``artifacts/models/``.

Example
-------
>>> from src.model_training import ModelTraining
>>> trainer = ModelTraining()
>>> trainer.run()
"""

from __future__ import annotations

# -------------------------------------------------------------------
# Standard & third-party imports
# -------------------------------------------------------------------
import os
import joblib
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

# -------------------------------------------------------------------
# Internal imports
# -------------------------------------------------------------------
from src.logger import get_logger
from src.custom_exception import CustomException

# -------------------------------------------------------------------
# Logger setup
# -------------------------------------------------------------------
logger = get_logger(__name__)


# -------------------------------------------------------------------
# Class: ModelTraining
# -------------------------------------------------------------------
class ModelTraining:
    """
    Handles training and evaluation of the Decision Tree classifier.

    Attributes
    ----------
    processed_data_path : str
        Directory containing preprocessed feature/target datasets.
    model_path : str
        Directory for saving the trained model and confusion matrix plot.
    model : DecisionTreeClassifier
        The classifier used for training and inference.
    """

    def __init__(self) -> None:
        # Directory where preprocessed data is stored
        self.processed_data_path: str = "artifacts/processed"

        # Directory where model outputs will be saved
        self.model_path: str = "artifacts/models"

        # Ensure the model directory exists
        os.makedirs(self.model_path, exist_ok=True)

        # Initialise the model
        self.model: DecisionTreeClassifier = DecisionTreeClassifier(
            criterion="gini", max_depth=30, random_state=42
        )

        logger.info("ModelTraining initialised successfully.")

    # -------------------------------------------------------------------
    # Method: load_data
    # -------------------------------------------------------------------
    def load_data(self):
        """
        Load preprocessed training and test datasets.

        Returns
        -------
        Tuple of pd.DataFrame and pd.Series
            (X_train, X_test, y_train, y_test)

        Raises
        ------
        CustomException
            If any dataset fails to load.
        """
        try:
            # Load datasets from the processed artifacts directory
            X_train = joblib.load(os.path.join(self.processed_data_path, "X_train.pkl"))
            X_test = joblib.load(os.path.join(self.processed_data_path, "X_test.pkl"))
            y_train = joblib.load(os.path.join(self.processed_data_path, "y_train.pkl"))
            y_test = joblib.load(os.path.join(self.processed_data_path, "y_test.pkl"))

            logger.info("Processed data loaded successfully.")
            return X_train, X_test, y_train, y_test

        except Exception as e:
            logger.error("Error while loading processed data: %s", e)
            raise CustomException("Failed to load processed data", e)

    # -------------------------------------------------------------------
    # Method: train_model
    # -------------------------------------------------------------------
    def train_model(self, X_train, y_train) -> None:
        """
        Fit the Decision Tree classifier on training data and save the model.

        Parameters
        ----------
        X_train : pd.DataFrame
            Training features.
        y_train : pd.Series
            Training target labels.

        Raises
        ------
        CustomException
            If training or model saving fails.
        """
        try:
            # Fit the model to training data
            self.model.fit(X_train, y_train)

            # Persist the trained model
            joblib.dump(self.model, os.path.join(self.model_path, "model.pkl"))

            logger.info("Model trained and saved successfully.")

        except Exception as e:
            logger.error("Error during model training: %s", e)
            raise CustomException("Failed to train model", e)

    # -------------------------------------------------------------------
    # Method: evaluate_model
    # -------------------------------------------------------------------
    def evaluate_model(self, X_test, y_test) -> None:
        """
        Evaluate the trained model on test data and generate a confusion matrix.

        Parameters
        ----------
        X_test : pd.DataFrame
            Test features.
        y_test : pd.Series
            True labels for the test set.

        Raises
        ------
        CustomException
            If evaluation or plotting fails.
        """
        try:
            # Generate predictions
            y_pred = self.model.predict(X_test)

            # Compute evaluation metrics
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average="weighted")
            recall = recall_score(y_test, y_pred, average="weighted")
            f1 = f1_score(y_test, y_pred, average="weighted")

            # Log the metrics for reference
            logger.info(f"Accuracy Score  : {accuracy:.4f}")
            logger.info(f"Precision Score : {precision:.4f}")
            logger.info(f"Recall Score    : {recall:.4f}")
            logger.info(f"F1 Score        : {f1:.4f}")

            # Compute confusion matrix
            cm = confusion_matrix(y_test, y_pred)

            # Create the confusion matrix plot
            plt.figure(figsize=(8, 6))
            sns.heatmap(
                cm,
                annot=True,
                cmap="Blues",
                fmt="d",
                xticklabels=np.unique(y_test),
                yticklabels=np.unique(y_test),
            )
            plt.title("Confusion Matrix")
            plt.xlabel("Predicted Label")
            plt.ylabel("Actual Label")

            # Save the confusion matrix to disk
            confusion_matrix_path = os.path.join(self.model_path, "confusion_matrix.png")
            plt.savefig(confusion_matrix_path)
            plt.close()

            logger.info("Confusion matrix saved successfully.")

        except Exception as e:
            logger.error("Error during model evaluation: %s", e)
            raise CustomException("Failed to evaluate model", e)

    # -------------------------------------------------------------------
    # Method: run
    # -------------------------------------------------------------------
    def run(self) -> None:
        """
        Execute the full model training workflow.

        Steps
        -----
        1. Load processed data.
        2. Train the Decision Tree model.
        3. Evaluate the model and save results.
        """
        # Load preprocessed training and test data
        X_train, X_test, y_train, y_test = self.load_data()

        # Train the model on training data
        self.train_model(X_train, y_train)

        # Evaluate the model and log metrics
        self.evaluate_model(X_test, y_test)


# -------------------------------------------------------------------
# Script entrypoint
# -------------------------------------------------------------------
if __name__ == "__main__":
    # Instantiate and run the model training pipeline
    trainer = ModelTraining()
    trainer.run()