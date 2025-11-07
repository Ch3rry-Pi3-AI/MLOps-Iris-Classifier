# 🔁 **`.circleci/` Folder — Continuous Integration and Deployment (CI/CD)**

The `.circleci/` directory contains the **CircleCI configuration** for the **MLOps Iris Classifier** project.
It automates the build, containerisation, and deployment of the Iris prediction pipeline to **Google Kubernetes Engine (GKE)** using a **Dockerised workflow** managed by **Google Cloud SDK**.

## 📁 **Folder Overview**

```text
.circleci/
└─ config.yml    # ⚙️ Defines the CI/CD pipeline for automated build and deployment
```

## 🧩 **Purpose**

The CircleCI configuration (`config.yml`) orchestrates the following automated processes:

| Stage | Operation              | Description                                                                              |
| ----: | ---------------------- | ---------------------------------------------------------------------------------------- |
|   1️⃣ | **Checkout Code**      | Pulls the latest repository code into the build environment.                             |
|   2️⃣ | **Build Docker Image** | Builds a Docker image of the Iris application and pushes it to Google Artifact Registry. |
|   3️⃣ | **Deploy to GKE**      | Connects to a GKE cluster and applies Kubernetes manifests for deployment.               |

Together, these steps ensure that every code change is **tested, built, containerised, and deployed** automatically and consistently.

## ⚙️ **Pipeline Configuration**

The CI/CD workflow is defined in **`config.yml`** using **CircleCI 2.1 syntax**.

### 🧱 Executor

```yaml
executors:
  docker-executor:
    docker:
      - image: google/cloud-sdk:latest
    working_directory: ~/repo
```

The executor uses the **Google Cloud SDK image**, allowing direct access to tools like `gcloud`, `docker`, and `kubectl`.

### 🧩 Jobs Overview

| Job                  | Description                                                                                               |
| -------------------- | --------------------------------------------------------------------------------------------------------- |
| `checkout_code`      | Clones the project repository into the build environment.                                                 |
| `build_docker_image` | Installs Docker, authenticates with GCP, builds the Docker image, and pushes it to **Artifact Registry**. |
| `deploy_to_gke`      | Authenticates with GCP, configures the target **GKE cluster**, and deploys using Kubernetes manifests.    |

### 🧠 **Workflow Definition**

```yaml
workflows:
  version: 2
  deploy_pipeline:
    jobs:
      - checkout_code
      - build_docker_image:
          requires:
            - checkout_code
      - deploy_to_gke:
          requires:
            - build_docker_image
```

This ensures that:

1. The repository is checked out first.
2. The Docker image is built and pushed.
3. The deployment occurs only after a successful image build.

## 🔒 **Environment Variables**

To keep credentials secure, CircleCI relies on **environment variables** stored in your project settings:

| Variable                | Purpose                                                                  |
| ----------------------- | ------------------------------------------------------------------------ |
| `GCLOUD_SERVICE_KEY`    | Base64-encoded Google Cloud service account key used for authentication. |
| `GOOGLE_PROJECT_ID`     | ID of the target Google Cloud project.                                   |
| `GOOGLE_COMPUTE_REGION` | Region where the GKE cluster resides.                                    |
| `GKE_CLUSTER`           | Name of the target Kubernetes cluster.                                   |

These are injected into the build environment at runtime.

## 🚀 **Deployment Process**

Once a commit is pushed to the repository, CircleCI automatically:

1. **Checks out** the latest code.
2. **Builds** a Docker image for the Iris app.
3. **Authenticates** with Google Cloud using a service account key.
4. **Pushes** the image to **Artifact Registry** (`us-central1-docker.pkg.dev`).
5. **Deploys** the updated application to **Google Kubernetes Engine (GKE)** via `kubectl apply -f kubernetes-deployment.yaml`.

✅ Successful completion ensures the latest version of your app is live in the Kubernetes cluster.

## 🧩 **Example Workflow Output**

```console
==== Starting CircleCI Deploy Pipeline ====
Checking out repository...
Installing Docker CLI...
Authenticated with Google Cloud successfully.
Building Docker image mlops-iris:latest...
Pushing to Artifact Registry...
Authenticating to GKE cluster...
Applying Kubernetes manifests...
Deployment successful!
```

## 📦 **Integration Summary**

| File                         | Purpose                                                       |
| ---------------------------- | ------------------------------------------------------------- |
| `.circleci/config.yml`       | Defines the entire CI/CD automation process.                  |
| `kubernetes-deployment.yaml` | (In project root) Describes deployment configuration for GKE. |
| `Dockerfile`                 | Defines how the project’s container image is built.           |

## ✅ **In Summary**

The `.circleci/` folder enables **continuous integration and deployment** for the MLOps Iris Classifier, automating the transition from code to cloud.
With every new commit, the project is **built, packaged, and deployed** seamlessly — ensuring versioned, reproducible, and production-ready MLOps workflows.

This configuration forms the **DevOps backbone** of the project, bridging **data science**, **model training**, and **cloud deployment** within a single automated pipeline.
