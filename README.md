# CI/CD Pipelines for Flask Python Application

## Project Overview

This project demonstrates two industry-standard Continuous Integration and Continuous Deployment (CI/CD) solutions for a Python Flask web application:

1. **Jenkins CI/CD Pipeline**
2. **GitHub Actions CI/CD Pipeline**

Both pipelines automate the software delivery lifecycle by installing dependencies, executing unit tests, building the application, and deploying it to staging or production environments.

---

# Project Objectives

- Automate software build, testing, and deployment.
- Implement CI/CD using Jenkins and GitHub Actions.
- Execute automated unit tests using Pytest.
- Deploy automatically to staging and production environments.
- Secure deployment credentials using GitHub Secrets and Jenkins Credentials.
- Configure automatic pipeline execution on every code change.

---

# Technology Stack

| Technology | Version |
|------------|----------|
| Python | 3.x |
| Flask | Latest |
| Jenkins | Latest LTS |
| GitHub Actions | Latest |
| Git | Latest |
| Pytest | Latest |
| Pip | Latest |
| Ubuntu | 22.04 LTS |

---

# Python Repository

https://github.com/GohelG/flask-cicd-app.git

---

# Repository Structure

```
flask-app/

├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
├── Jenkinsfile
├── app.py
├── requirements.txt
├── tests/
│   └── test_app.py
├── README.md
└── .gitignore
```

---

# Branch Structure

```
main
staging
```

| Branch | Purpose |
|----------|----------|
| main | Production |
| staging | Testing |

---

# Prerequisites

Install the following software before starting.

- Ubuntu Server
- Git
- Python 3
- pip
- Virtual Environment
- Jenkins
- Java 17
- GitHub Account

---

# Jenkins CI/CD Pipeline

# Installation Guide

## Install Jenkins

### Update Package Lists

```bash
sudo apt update
```

### Install Required Dependencies

```bash
sudo apt install -y wget curl gnupg
```

### Add Jenkins GPG Key

```bash
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | \
sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
```

### Add Jenkins Repository

```bash
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | \
sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
```

### Install Java

```bash
sudo apt update
sudo apt install -y fontconfig openjdk-17-jre
```

### Install Jenkins

```bash
sudo apt update
sudo apt install -y jenkins
```

### Start Jenkins Service

```bash
sudo systemctl enable jenkins
sudo systemctl start jenkins
sudo systemctl status jenkins
```

### Unlock Jenkins

Open your browser:

```
http://localhost:8080
```

Retrieve the initial administrator password:

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

---

# Install Git

### Update Package Lists

```bash
sudo apt update
```

### Install Git

```bash
sudo apt install git -y
```

### Verify Installation

```bash
git --version
```

### Install Latest Git (Optional)

```bash
sudo add-apt-repository ppa:git-core/ppa -y
sudo apt update
sudo apt install git -y
```

### Configure Git

```bash
git config --global user.name "Your Name"

git config --global user.email "youremail@example.com"
```

### Verify Configuration

```bash
git config --global --list
```

---

# Install Python 3

### Update Package Lists

```bash
sudo apt update
```

### Install Python

```bash
sudo apt install python3-full python3-pip python3-venv python3-pytest -y
```

### Create Virtual Environment

```bash
python3 -m venv .venv
```

### Activate Virtual Environment

```bash
source .venv/bin/activate
```

### Install Required Python Packages

```bash
pip install --upgrade pip
pip install pytest
```

### Verify Installation

```bash
python3 --version

pip3 --version

pytest --version
```

---

# Install MongoDB 8.x

### Install Dependencies

```bash
sudo apt update
sudo apt install -y gnupg curl
```

### Import MongoDB GPG Key

```bash
curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc | \
sudo gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg --dearmor
```

### Add MongoDB Repository

```bash
echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.2 multiverse" | \
sudo tee /etc/apt/sources.list.d/mongodb-org-8.2.list
```

### Install MongoDB

```bash
sudo apt update
sudo apt install -y mongodb-org
```

### Start MongoDB

```bash
sudo systemctl enable mongod
sudo systemctl start mongod
sudo systemctl status mongod
```

### Verify MongoDB

```bash
mongosh
```

_Note: If the MongoDB shell opens successfully, MongoDB is installed and running._

## Required Jenkins Plugins

- Git
- GitHub
- Pipeline
- Email Extension
- SSH Agent
- Workspace Cleanup
- Blue Ocean (Optional)

---

## Jenkins Pipeline Stages

### Checkout

Clone source code from GitHub.

### Build

```bash
python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

### Test

```bash
pytest
```

### Deploy

Deploy to staging server.

Example

```bash
scp -r . jenkins@jenkins-server-public-ip:/var/www/flask-app
```

---

## Configure Jenkins Job

1. Create Pipeline Project
2. Select Pipeline Script from SCM
3. Repository URL
4. Branch = main
5. Script Path = Jenkinsfile

---

## Jenkins Trigger

Configure GitHub Webhook.

```
http://jenkins-server-public-ip:8080/github-webhook/
```

Trigger

```
Push Event
```

---

## Jenkins Email Notification

Configure SMTP under

```
Manage Jenkins

↓

Configure System
```

Example

```
SMTP Server

smtp.gmail.com

Port

587
```

Notifications sent for

- Build Success
- Build Failure

---

# GitHub Actions CI/CD Pipeline

## Workflow Location

```
.github/workflows/ci-cd.yml
```

---

## Workflow Triggers

| Event | Action |
|----------|------------|
| Pull Request | Build & Test |
| Push to staging | Deploy to Staging |
| Release Tag | Deploy to Production |

---

## Workflow Jobs

### Checkout

```yaml
actions/checkout@v4
```

---

### Setup Python

```yaml
actions/setup-python@v5
```

---

### Install Dependencies

```bash
python -m pip install --upgrade pip

pip install -r requirements.txt
```

---

### Run Tests

```bash
pytest
```

---

### Build

Example

```bash
python setup.py sdist
```

---

### Deploy to Staging

Executed only on

```
staging
```

Example

```bash
scp -r . jenkins@jenkins-server-public-ip:/var/www/flask-app
```

---

### Deploy to Production

Executed only when a GitHub Release is published.

---

# GitHub Secrets

Go to

```
Repository

↓

Settings

↓

Secrets and Variables

↓

Actions
```

Create the following secrets.

| Secret | Description |
|------------|----------------|
| STAGING_HOST | Server IP |
| STAGING_USER | SSH User |
| STAGING_KEY | SSH Private Key |
| PRODUCTION_HOST | Production IP |
| PRODUCTION_USER | Production User |
| PRODUCTION_KEY | Production SSH Key |
| DEPLOY_PATH | Deployment Directory |

---

# CI/CD Workflow

```
Developer

        │

        ▼

GitHub Repository

        │

        ▼

──────────────────────────────

Jenkins Pipeline

Checkout

↓

Build

↓

Install Dependencies

↓

Run Tests

↓

Deploy to Staging

↓

Email Notification

──────────────────────────────

OR

──────────────────────────────

GitHub Actions

Checkout

↓

Setup Python

↓

Install Dependencies

↓

Run Tests

↓

Build

↓

Deploy to Staging

↓

Deploy to Production

──────────────────────────────
```

---

# Running Jenkins Pipeline

```bash
git add .

git commit -m "Updated application"

git push origin main
```

---

# Running GitHub Actions Pipeline

Push changes to staging.

```bash
git add .

git commit -m "Testing GitHub Actions"

git push origin staging
```

---

# Production Deployment

Create a release tag.

```bash
git tag v1.0.0

git push origin v1.0.0
```

or publish a GitHub Release.

---

# Expected Output

### Jenkins

- Clone Repository
- Install Dependencies
- Run Tests
- Deploy to Staging
- Email Notification

### GitHub Actions

- Checkout Repository
- Setup Python
- Install Dependencies
- Execute Pytest
- Build Application
- Deploy to Staging
- Deploy to Production

---

# Screenshots to Include

## Jenkins

- Jenkins Dashboard
- Pipeline Configuration
- Successful Build
- Console Output
- Email Notification

---

## GitHub Actions

- Repository Home
- Branches (main & staging)
- Workflow Running
- Successful Workflow
- Production Release Workflow
- GitHub Secrets (values hidden)

---

# Future Enhancements

- Docker Support
- Kubernetes Deployment
- SonarQube Integration
- Trivy Security Scanning
- AWS EC2 Deployment
- Azure VM Deployment
- GCP Deployment
- Slack Notifications
- Microsoft Teams Notifications
- Automatic Rollback

---

# Submission Checklist

- Jenkins Installed
- Jenkinsfile Created
- GitHub Actions Workflow Created
- README.md Updated
- Main & Staging Branches Available
- GitHub Secrets Configured
- Jenkins Credentials Configured
- Successful Jenkins Build
- Successful GitHub Actions Build
- Deployment Verified
- Screenshots Included

---

# Author

**Gautam Gohel**

**Cloud Engineer | DevOps Engineer | System Administrator**
````