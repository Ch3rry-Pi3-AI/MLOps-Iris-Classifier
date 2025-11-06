"""
data_processing.py
==================
Implements the ``DataProcessing`` class for the Iris classification workflow.

Overview
--------
This module provides a minimal data-preparation stage used in the project setup.
It:
1) Loads a CSV dataset from disk
2) Handles outliers in a specified numeric column using the IQR rule
3) Splits the data into train/test sets
4) Persists splits to ``artifacts/processed/`` using Joblib

Notes
-----
- Outlier handling follows the 1.5 * IQR rule and replaces detected outliers
  with the column median. The implementation mirrors the original logic,
  including value-by-value replacement (kept intentionally for parity).
- Saved artefacts:
  * ``X_train.pkl``, ``X_test.pkl`` — feature matrices
  * ``y_train.pkl``, ``y_test.pkl`` — target vectors

Examples
--------
>>> dp = DataProcessing("artifacts/raw/data.csv")
>>> dp.run()
"""

from __future__ import annotations

# -------------------------------------------------------------------
# Standard & third-party imports
# -------------------------------------------------------------------
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

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
# Class: DataProcessing
# -------------------------------------------------------------------
class DataProcessing:
    """
    Simple, reproducible data-processing pipeline for Iris.

    Parameters
    ----------
    file_path : str
        Path to the input CSV file (e.g., ``artifacts/raw/data.csv``).

    Attributes
    ----------
    file_path : str
        Source CSV path.
    df : pd.DataFrame | None
        In-memory dataframe after loading.
    processed_data_path : str
        Directory where processed artefacts are persisted.
    """

    def __init__(self, file_path: str) -> None:
        # Store incoming CSV path
        self.file_path: str = file_path

        # Placeholder for the loaded dataframe
        self.df: pd.DataFrame | None = None

        # Location for persisted outputs
        self.processed_data_path: str = "artifacts/processed"

        # Ensure the output directory exists
        os.makedirs(self.processed_data_path, exist_ok=True)

    # -------------------------------------------------------------------
    # Method: load_data
    # -------------------------------------------------------------------
    def load_data(self) -> None:
        """
        Load the dataset from ``self.file_path`` into ``self.df``.

        Raises
        ------
        CustomException
            If the CSV cannot be read.
        """
        try:
            # Read CSV into a dataframe
            self.df = pd.read_csv(self.file_path)

            # Log success with basic shape info
            logger.info("Data read successfully. Shape: %s", None if self.df is None else self.df.shape)
        except Exception as e:
            # Log the error for debugging
            logger.error("Error while reading data %s", e)

            # Re-raise using the project's custom exception (call pattern preserved)
            raise CustomException("Failed to read data", e)

    # -------------------------------------------------------------------
    # Method: handle_outliers
    # -------------------------------------------------------------------
    def handle_outliers(self, column: str) -> None:
        """
        Replace outliers in ``column`` using the 1.5 * IQR rule with the column median.

        Parameters
        ----------
        column : str
            Name of the numeric column on which to perform outlier handling.

        Raises
        ------
        CustomException
            If the operation fails.
        """
        try:
            # Log start of operation
            logger.info("Starting outlier handling for column: %s", column)

            # Compute first and third quartiles
            Q1 = self.df[column].quantile(0.25)
            Q3 = self.df[column].quantile(0.75)

            # Interquartile range
            IQR = Q3 - Q1

            # Bounds for outliers
            Lower_value = Q1 - 1.5 * IQR
            Upper_value = Q3 + 1.5 * IQR

            # Median used for replacement
            sepal_median = np.median(self.df[column])

            # Iterate over values (kept intentionally to match original logic)
            for i in self.df[column]:
                # If value falls outside bounds, replace with median
                if i > Upper_value or i < Lower_value:
                    self.df[column] = self.df[column].replace(i, sepal_median)

            # Log successful completion
            logger.info("Outliers handled successfully for column: %s", column)

        except Exception as e:
            # Log the error for debugging
            logger.error("Error while handling outliers %s", e)

            # Re-raise using the project's custom exception (call pattern preserved)
            raise CustomException("Failed to handle outliers", e)

    # -------------------------------------------------------------------
    # Method: split_data
    # -------------------------------------------------------------------
    def split_data(self) -> None:
        """
        Split features/target into train/test sets and persist them to disk.

        Notes
        -----
        - Feature columns are the four Iris measurements:
          ``['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']``.
        - Target column is ``'Species'``.

        Raises
        ------
        CustomException
            If the split or persistence fails.
        """
        try:
            # Select the four numeric feature columns
            X = self.df[["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"]]

            # Select the target column
            Y = self.df["Species"]

            # Perform the train/test split with a fixed seed for reproducibility
            X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

            # Log that the split succeeded
            logger.info("Data split successfully into train/test.")

            # Persist splits to the processed artefacts directory
            joblib.dump(X_train, os.path.join(self.processed_data_path, "X_train.pkl"))
            joblib.dump(X_test, os.path.join(self.processed_data_path, "X_test.pkl"))
            joblib.dump(y_train, os.path.join(self.processed_data_path, "y_train.pkl"))
            joblib.dump(y_test, os.path.join(self.processed_data_path, "y_test.pkl"))

            # Log successful file saves
            logger.info("Processed files saved successfully for data-processing step.")

        except Exception as e:
            # Log the error for debugging
            logger.error("Error while splitting data %s", e)

            # Re-raise using the project's custom exception (call pattern preserved)
            raise CustomException("Failed to split data", e)

    # -------------------------------------------------------------------
    # Method: run
    # -------------------------------------------------------------------
    def run(self) -> None:
        """
        Execute the full pipeline in order:
        1) Load data
        2) Handle outliers in ``SepalWidthCm``
        3) Split and persist datasets
        """
        # Load the CSV
        self.load_data()

        # Apply the IQR-based outlier handling on the specified column
        self.handle_outliers("SepalWidthCm")

        # Split into train/test and save artefacts
        self.split_data()


# -------------------------------------------------------------------
# Script entrypoint
# -------------------------------------------------------------------
if __name__ == "__main__":
    # Default input path for the raw Iris data
    data_processor = DataProcessing("artifacts/raw/data.csv")

    # Run the pipeline end-to-end
    data_processor.run()
