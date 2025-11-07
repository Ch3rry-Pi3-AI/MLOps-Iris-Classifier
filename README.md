# 🌺 **MLOps Iris Classifier — End-to-End CI/CD Deployment**

This repository demonstrates a **complete MLOps workflow** using the classic **Iris dataset**, progressing from data preprocessing and model training to full web deployment through an automated **CI/CD (Continuous Integration and Continuous Deployment)** pipeline built with **CircleCI**.

<p align="center">
  <img src="img/flask/flask_app.png" alt="Deployed Flask Iris Classifier Application" style="width:100%; height:auto;" />
</p>

While the machine learning use case — **Iris species classification** — is intentionally simple, the project’s main objective is to showcase a **modern, production-grade MLOps workflow** using **CircleCI** for pipeline automation, containerisation, and cloud deployment.

## 🧩 **Project Overview**

This project guides the full lifecycle of a machine learning system — from raw data to live deployment — following a modular, reproducible, and production-aligned architecture.
Each stage builds upon the previous one, ensuring traceability, automation, and scalability.

### 🌱 **Stage 00 — Project Setup**

The foundation was established with a structured repository layout (`src/`, `pipeline/`, `artifacts/`, etc.), dependency management via **`uv`**, and environment setup for consistent development.

### 💾 **Stage 01 — Data Processing**

The **`data_processing.py`** module handled:

* Loading the Iris dataset
* Cleaning and handling outliers
* Splitting into training and test sets
* Saving processed artefacts for downstream use

This ensured that all preprocessing steps were fully reproducible and logged.

### 🧠 **Stage 02 — Model Training**

The **`model_training.py`** module trained a **Decision Tree Classifier**, evaluated performance (accuracy, precision, recall, F1), and saved both the model (`model.pkl`) and confusion matrix.
All actions were logged and wrapped with robust exception handling.

### 🌸 **Stage 03 — Flask Application**

A **Flask web app** was developed to serve the trained model through a user-friendly interface.
Users can input sepal and petal measurements and receive real-time species predictions.
This stage introduced:

* A responsive UI (`templates/index.html`)
* Clean styling (`static/style.css`)
* Live model inference served via `app.py`

<p align="center">
  <img src="img/flask/flask_app.png" alt="Flask App Interface" style="width:100%; height:auto;" />
</p>

### ⚙️ **Stage 04 — Training Pipeline**

The **`pipeline/training_pipeline.py`** module unified data processing and model training into a single automated script, ensuring consistent execution and end-to-end logging.
This stage introduced modular orchestration, preparing the groundwork for CI/CD integration.

### 🚀 **Stage 05 — CI/CD Deployment (CircleCI)**

Finally, the project was extended into a **CI/CD pipeline** — short for **Continuous Integration and Continuous Deployment** — using **CircleCI**.
Each new commit triggers the following workflow automatically:

1. **Build** a Docker image for the Flask application.
2. **Push** it to **Google Artifact Registry**.
3. **Deploy** to **Google Kubernetes Engine (GKE)** as a managed cluster.

The pipeline is defined in `.circleci/config.yml`, while deployment configuration lives in `kubernetes-deployment.yaml`.


## 💡 **Why CircleCI?**

This project deliberately uses **CircleCI** instead of **Jenkins** to demonstrate a simpler, more modern approach to CI/CD.

### ✅ **Key Advantages of CircleCI**

* **Faster setup:** No server installation — entirely cloud-hosted.
* **Simple configuration:** YAML-based workflows are clean, modular, and easy to maintain.
* **Integrated environment variables:** Secure handling of credentials like GCP service keys.
* **Seamless cloud integration:** Direct authentication and deployment to **GCP**, **AWS**, and **Azure**.
* **Speed and caching:** Builds are significantly faster with built-in caching and Docker layer reuse.
* **Ease of collaboration:** Automatically integrates with GitHub repositories and triggers on every commit.

Overall, **CircleCI offers a lightweight, scalable, and highly maintainable alternative to Jenkins** for managing modern MLOps workflows.


## 🗂️ **Final Project Structure**

```text
mlops_iris_classifier/
├── .circleci/                    # CircleCI configuration for CI/CD automation
│   └── config.yml
├── artifacts/                    # Data, processed artefacts, and model outputs
│   ├── raw/
│   ├── processed/
│   └── models/
├── pipeline/
│   └── training_pipeline.py       # Unified orchestration of data processing + training
├── src/
│   ├── data_processing.py
│   ├── model_training.py
│   ├── logger.py
│   └── custom_exception.py
├── templates/
│   └── index.html                 # Flask front-end UI
├── static/
│   ├── style.css
│   └── img/app_background.jpg
├── img/
│   ├── flask/flask_app.png
│   └── circle_ci/
├── Dockerfile                     # Container image definition for Flask app
├── kubernetes-deployment.yaml     # Kubernetes Deployment + Service configuration
├── app.py                         # Flask application entry point
├── pyproject.toml                 # Project metadata
├── setup.py                       # Editable install support
└── requirements.txt               # Dependencies
```

## 🌐 **End-to-End Workflow Summary**

1. **Data Ingestion & Preprocessing** → clean, split, and save artefacts.
2. **Model Training** → fit, evaluate, and export model artefacts.
3. **Flask Deployment** → serve predictions through a local web interface.
4. **Pipeline Orchestration** → automate full data + training execution.
5. **CI/CD Integration** → deploy Dockerised app to Kubernetes via CircleCI.

The entire lifecycle — from dataset to live web application — is **fully automated, reproducible, and version-controlled**.


## ✅ **In Summary**

This project transforms a basic Iris classification model into a **complete MLOps system**.
It demonstrates **how to operationalise machine learning workflows** through automation, containerisation, and deployment pipelines — culminating in a **production-ready CI/CD process** powered by **CircleCI**.

<p align="center">
  <img src="img/flask/flask_app.png" alt="Final Flask App Screenshot" style="width:100%; height:auto;" />
</p>
