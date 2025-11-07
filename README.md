Excellent — this will be the **final stage README** for your `MLOps Iris Classifier` project, covering the **complete CI/CD deployment** using **Docker, Kubernetes, and CircleCI**.
It’s written as a fully-documented, professional-grade guide, blending clear structure, step-by-step setup, and embedded screenshots from both `img/circle_ci/` and `img/flask/`.
Everything from enabling APIs to environment variables is covered precisely and in order.

---

# 🚀 **CI/CD Deployment — MLOps Iris Classifier**

This branch extends the **MLOps Iris Classifier** pipeline into a **fully automated CI/CD deployment** using **Docker**, **Kubernetes**, and **CircleCI**.
It represents the **fifth and final workflow stage**, where the trained model and Flask application are containerised, pushed to **Google Artifact Registry**, and deployed on **Google Kubernetes Engine (GKE)** — all triggered automatically from **CircleCI**.

<p align="center">
  <img src="img/flask/flask_app.png" alt="Deployed Flask Iris Classifier Application" width="720"/>
</p>

---

## 🧩 **Overview**

This stage integrates everything built so far — data processing, model training, Flask app deployment — into an end-to-end MLOps system with continuous integration and delivery.
CircleCI orchestrates the build → push → deploy workflow, ensuring every new commit automatically triggers:

1. Docker image build
2. Push to Artifact Registry
3. Deployment update in GKE

### 🔍 Core Components

| Component                       | Description                                                                 |
| ------------------------------- | --------------------------------------------------------------------------- |
| **Dockerfile**                  | Builds the container image for the Flask app.                               |
| **kubernetes-deployment.yaml**  | Defines Kubernetes Deployment and Service for the app.                      |
| **.circleci/config.yml**        | CI/CD pipeline that builds, pushes, and deploys automatically via CircleCI. |
| **Google Cloud Platform (GCP)** | Hosts the container registry and managed Kubernetes cluster (GKE).          |
| **CircleCI**                    | Handles build, authentication, and deployment automation.                   |

---

## 🗂️ **Updated Project Structure**

```text
mlops_iris_classifier/
├── .circleci/
│   └── config.yml                 # CircleCI pipeline configuration (build, push, deploy)
├── artifacts/
│   ├── raw/
│   ├── processed/
│   └── models/
├── pipeline/
│   └── training_pipeline.py       # Orchestrates data preparation and model training
├── src/
│   ├── data_processing.py
│   ├── model_training.py
│   ├── logger.py
│   └── custom_exception.py
├── templates/
│   └── index.html                 # Flask web app UI
├── static/
│   ├── style.css
│   └── img/app_background.jpg
├── img/
│   ├── flask/
│   │   └── flask_app.png          # Flask app preview
│   └── circle_ci/                 # CircleCI setup screenshots
│       ├── new_project.png
│       ├── select_project_option.png
│       ├── name_project.png
│       ├── choose_repo.png
│       ├── select_project_repo.png
│       ├── setup_config.png
│       ├── triggers.png
│       ├── pipeline_setup_success.png
│       ├── project_settings.png
│       ├── gcloud_service_key.png
│       ├── project_id.png
│       ├── successful_pipeline_run.png
│       ├── workloads.png
│       └── endpoint.png
├── Dockerfile                     # Container image for Flask app
├── kubernetes-deployment.yaml     # Kubernetes Deployment + Service definitions
├── app.py                         # Flask application entry point
├── pyproject.toml
├── setup.py
└── requirements.txt
```

---

## ☁️ **1. Google Cloud Platform Setup**

### Step 1: Enable Required APIs

Go to **GCP Console → Navigation Menu → APIs & Services → Library**, and enable the following APIs:

* **Kubernetes Engine API**
* **Google Container Registry API**
* **Compute Engine API**
* **Cloud Build API**
* **Cloud Storage API**
* **Identity and Access Management (IAM) API**

---

### Step 2: Create a GKE Cluster

1. In the GCP search bar, search for **“Kubernetes Engine”**.
2. Go to **Clusters → + Create**.
3. Choose the **Autopilot (managed)** option and click **Configure**.
4. Keep default settings for **Cluster Basics** and **Fleet registration**.
5. In **Networking**, ensure both:

   * ✅ “Access using DNS”
   * ✅ “Access using IPv4 addresses”
     are selected.
6. Click **Create** and wait for your cluster to provision.

---

### Step 3: Create a Service Account

1. Go to **IAM & Admin → Service Accounts → + CREATE SERVICE ACCOUNT**.
2. Name it: `mlops-iris`.
3. Click **Create and Continue**.
4. Grant the following roles:

   * **Owner**
   * **Storage Object Admin**
   * **Storage Object Viewer**
   * **Artifact Registry Administrator**
   * **Artifact Registry Writer**
5. Click **Done**.
6. Under **Actions → Manage Keys → Add Key → Create New Key**, choose **JSON format** and download it.
7. Move it to your project root and rename it:

   ```bash
   mv ~/Downloads/your-key.json gcp-key.json
   ```

---

### Step 4: Create an Artifact Registry

1. Go to **Navigation Menu → Artifact Registry**.
2. Click **+ CREATE REPOSITORY**.
3. Name it `mlops-iris`.
4. Choose region `us-central1` (or the region where your cluster is deployed).
5. Keep defaults and click **Create**.

---

## 🐳 **2. Docker and Kubernetes Setup**

### Step 1: Create the `Dockerfile`

```dockerfile
FROM python:3.12

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -e .

EXPOSE 5000
ENV FLASK_APP=app.py

CMD ["python", "app.py"]
```

---

### Step 2: Create `kubernetes-deployment.yaml`

```yaml
# Kubernetes Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mlops-iris
spec:
  replicas: 2
  selector:
    matchLabels:
      app: mlops-iris
  template:
    metadata:
      labels:
        app: mlops-iris
    spec:
      containers:
        - name: mlops-iris
          image: us-central1-docker.pkg.dev/sacred-garden-474511-b9/mlops-iris/mlops-iris:latest
          ports:
            - containerPort: 5000

# Kubernetes Service
---
apiVersion: v1
kind: Service
metadata:
  name: mlops-service
spec:
  selector:
    app: mlops-iris
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
  type: LoadBalancer
```

---

## 🔄 **3. CircleCI Setup**

### Step 1: Create `.circleci/config.yml`

Your pipeline should match the following:

```yaml
version: 2.1

executors:
  docker-executor:
    docker:
      - image: google/cloud-sdk:latest
    working_directory: ~/repo

jobs:
  checkout_code:
    executor: docker-executor
    steps:
      - checkout

  build_docker_image:
    executor: docker-executor
    steps:
      - checkout
      - setup_remote_docker
      - run:
          name: Install Docker CLI
          command: |
            apt-get update && apt-get install -y docker.io
      - run:
          name: Authenticate with Google Cloud
          command: |
            echo "$GCLOUD_SERVICE_KEY" | base64 --decode > gcp-key.json
            gcloud auth activate-service-account --key-file=gcp-key.json
            gcloud auth configure-docker us-central1-docker.pkg.dev --quiet
      - run:
          name: Build and Push Image
          command: |
            docker build -t us-central1-docker.pkg.dev/$GOOGLE_PROJECT_ID/mlops-iris/mlops-iris:latest .
            docker push us-central1-docker.pkg.dev/$GOOGLE_PROJECT_ID/mlops-iris/mlops-iris:latest

  deploy_to_gke:
    executor: docker-executor
    steps:
      - checkout
      - run:
          name: Authenticate with Google Cloud
          command: |
            echo "$GCLOUD_SERVICE_KEY" | base64 --decode > gcp-key.json
            gcloud auth activate-service-account --key-file=gcp-key.json
      - run:
          name: Configure GKE
          command: |
            gcloud container clusters get-credentials "$GKE_CLUSTER" \
              --region "$GOOGLE_COMPUTE_REGION" \
              --project "$GOOGLE_PROJECT_ID"
      - run:
          name: Deploy to GKE
          command: |
            kubectl apply -f kubernetes-deployment.yaml

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

---

### Step 2: Set Up CircleCI

1. Go to [https://circleci.com](https://circleci.com) and create a free account.
2. Create a new organisation → **New Project**.

<p align="center"><img src="img/circle_ci/new_project.png" width="600"/></p>

3. Select **“Build, test, and deploy your software application”**.

<p align="center"><img src="img/circle_ci/select_project_option.png" width="600"/></p>

4. Name your project.

<p align="center"><img src="img/circle_ci/name_project.png" width="600"/></p>

5. Choose your GitHub repository.

<p align="center"><img src="img/circle_ci/choose_repo.png" width="600"/></p>
<p align="center"><img src="img/circle_ci/select_project_repo.png" width="600"/></p>

6. CircleCI will detect `.circleci/config.yml`.

<p align="center"><img src="img/circle_ci/setup_config.png" width="600"/></p>

7. Leave default **Triggers** settings.

<p align="center"><img src="img/circle_ci/triggers.png" width="600"/></p>

8. Review and finish setup.

<p align="center"><img src="img/circle_ci/pipeline_setup_success.png" width="600"/></p>

---

## 🔐 **4. Configure Environment Variables in CircleCI**

### Step 1: Base64 Encode Your GCP Key

In a Bash terminal (from project root):

```bash
cat gcp-key.json | base64 -w 0
```

Copy the output string.

---

### Step 2: Add Environment Variables in CircleCI

Go to your CircleCI **Project Settings → Environment Variables**.

<p align="center"><img src="img/circle_ci/project_settings.png" width="600"/></p>

Add the following variables:

| Name                    | Value                                                |
| ----------------------- | ---------------------------------------------------- |
| `GCLOUD_SERVICE_KEY`    | (paste base64-encoded key)                           |
| `GOOGLE_PROJECT_ID`     | your GCP project ID (e.g. `sacred-garden-474511-b9`) |
| `GKE_CLUSTER`           | your GKE cluster name (e.g. `autopilot-cluster-1`)   |
| `GOOGLE_COMPUTE_REGION` | your compute region (e.g. `us-central1`)             |

<p align="center"><img src="img/circle_ci/gcloud_service_key.png" width="600"/></p>
<p align="center"><img src="img/circle_ci/project_id.png" width="600"/></p>

---

## ⚙️ **5. Trigger the CI/CD Pipeline**

Back in CircleCI, click **“Trigger Pipeline”**.

<p align="center"><img src="img/circle_ci/successful_pipeline_run.png" width="600"/></p>

After a successful run, your application will have been automatically deployed to **Google Kubernetes Engine**.

---

## ☸️ **6. Verify Deployment in GKE**

1. Go to **Kubernetes Engine → Workloads**.
   You should see your running deployment:

<p align="center"><img src="img/circle_ci/workloads.png" width="600"/></p>

2. Click on `mlops-iris` to view workload details.
3. Scroll down to **Exposing Services**, and you’ll see the public **Endpoint URL**:

<p align="center"><img src="img/circle_ci/endpoint.png" width="600"/></p>

4. Click the endpoint — your Iris Classifier Flask app is now live:

<p align="center"><img src="img/flask/flask_app.png" width="720"/></p>

---

## ✅ **In Summary**

| Stage                     | Description                                         |
| ------------------------- | --------------------------------------------------- |
| **Data & Model Pipeline** | Fully automated via `pipeline/training_pipeline.py` |
| **Containerisation**      | Dockerised Flask app with model and assets          |
| **Deployment**            | GKE-managed Kubernetes cluster via CircleCI         |
| **Automation**            | CI/CD pipeline triggers on push to main branch      |
| **Access**                | Public endpoint via LoadBalancer service            |

Your **MLOps Iris Classifier** is now a complete **end-to-end production pipeline**, from dataset → model → container → CI/CD → live deployment.
Every component is **automated, versioned, and reproducible** — the true hallmark of a production-ready MLOps system.
