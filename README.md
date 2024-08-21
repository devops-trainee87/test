# **Coffee API Service Documentation**

## **Table of Contents**

1. [Overview](#1-overview)
2. [Prerequisites](#2-prerequisites)
3. [Infrastructure as Code (IaC) Setup](#3-infrastructure-as-code-iac-setup)
4. [Deployment Application](#4-deployment-application)
    - [Dockerizing the API](#dockerizing-the-api)
    - [Deploying to Minikube](#deploying-to-minikube)
5. [Usage Instructions](#5-usage-instructions)

---

## **1. Overview**

The Coffee API Service is a RESTful API designed to simulate a simple coffee-selling platform. Users can "purchase" different types of coffee based on the payment amount provided:

- **Espresso**: For payments less than $2.00.
- **Latte**: For payments between $2.00 and $3.00.
- **Cappuccino**: For payments of $3.00 or more.

The API is built using FastAPI and integrates with a PostgreSQL database to record transactions. Each transaction logs details such as the transaction ID, timestamp, payment amount, and the type of coffee served.

The service is containerized using Docker and deployed on a Kubernetes cluster via Minikube for local development. Deployment and management are automated through GitHub Actions, ensuring that the service is easy to maintain and scale.

---

## **2. Prerequisites**

Before deploying the Coffee API Service, ensure that you have the following installed and configured:

- [**Git**](https://git-scm.com/download/linux): Version control system.
- [**Docker**](https://docs.docker.com/engine/install/): Containerization platform.
- [**Terraform**](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli): Infrastructure as Code tool.
- [**Minikube**](https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fbinary+download): Local Kubernetes cluster or you can use your Kubernetes cluster.
- [**kubectl**](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/): Kubernetes command-line tool.
- [**GitHub account**](https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github): Required for creating repositories and running CI/CD pipelines. You can use your existing account.

---

## **3. Infrastructure as Code (IaC) Setup**

### **Terraform Setup**

1. **Clone the Infrastructure Repository**:
   ```bash
   git clone <infra-repo-url>
   cd infra

2. **Terraform Configuration**:

- **main.tf**: Automates the creation of a GitHub repository, sets up branch protection, and configures secrets and environment variables.
- **variables.tf**: Contains variables *db_user*, *db_name*, *db_host* that you can change. Do not specify the database password and GitHub token to prevent leakage.

3. **Creating GitHub working repository in your account**:
   ```bash
   terraform init
   terraform apply
   ```
   This setup creates the necessary GitHub repository with protected branches and secrets. You will be prompted to enter the database password and GitHub token.

---
## **4. Deployment Application**

### **Dockerizing the API**

   ```bash
   docker build -t <your docker repo/your container tag> .
   docker push <your docker repo/your container tag>
   ```

### **Deploying to minikube**:
   ```bash
   kubectl create ns coffee-app #create namespace
   kubectl create configmap -n coffee-app coffee-app-config --from-env-file=.env  #create configmap from .env file
   kubectl create secret generic -n coffee-app coffee-app-secret --from-literal=POSTGRES_PASSWORD=<password> #create secret with database password
   kubectl apply -f k8s/postgres-deployment.yaml #db deployment
   ```
   Specify your image name in the *k8s/kustomization.yaml* in the *newName* field and run
   ```bash
   kubectl -k k8s/ #API deployment
   ```
### **Access the Service**:
   ```bash
   minikube service coffee-api-service --url -n coffee-app
   ```
   This command will provide the URL to access the Coffee API service.

## **5. Usage Instructions**

   Once the service is deployed, you can interact with the Coffee API by sending HTTP requests. For example:

   - Get Coffee Type Based on Payment:
   ```bash
   curl -X POST "http://<minikube-url>/buy_coffee" -H "Content-Type: application/json" -d '{"amount": 2.5}'
   ```
   - Response: {"transaction_id": <transaction_id>,"coffee_type":"Latte","payment_amount":2.5}

## **6. GitHub Actions CI/CD Pipeline**

   Project includes workflow file .github/workflows/main.yml with the following stages:
   - Secret Scan: Uses [**gitleaks**](https://github.com/gitleaks/gitleaks) to scan for secrets.
   - Build and Push Docker Image: Builds Docker images and pushes them to GitHub Packages.
   - Run Tests: Executes unit and integration tests (if you add this tests).
   - Deploy to Minikube: Deploys the application to Minikube and verifies it with curl.

   Push your code to the *env/staging* or *main* branches of the repository created on [this step](#terraform-setup) to trigger the CI/CD pipeline.
