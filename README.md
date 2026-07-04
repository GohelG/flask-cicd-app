# CI/CD Pipelines for Flask Python Application

## Project Overview

This project demonstrates two industry-standard Continuous Integration and Continuous Deployment (CI/CD) solutions for a Python Flask web application:

1. **Jenkins CI/CD Pipeline**
2. **GitHub Actions CI/CD Pipeline**

Both pipelines automate the software delivery lifecycle by installing dependencies, executing unit tests, building the application, and deploying it to staging or production environments.

---

## Project Objectives
- Automate software build, testing, and deployment.
- Implement CI/CD using Jenkins and GitHub Actions.
- Execute automated unit tests using Pytest.
- Deploy automatically to staging and production environments.
- Secure deployment credentials using GitHub Secrets and Jenkins Credentials.
- Configure automatic pipeline execution on every code change.

---

## Architecture Diagram

'''
                    Developer
                        │
                Git Push / Pull Request
                        │
                        ▼
                GitHub Repository
                        │
      ┌─────────────────┴─────────────────┐
      │                                   │
      ▼                                   ▼
 Jenkins Pipeline                 GitHub Actions
      │                                   │
 Checkout                         Checkout
      │                                   │
 Install Dependencies             Setup Python
      │                                   │
 Run Unit Tests                   Run Unit Tests
      │                                   │
 Build                            Build
      │                                   │
 Deploy                           Deploy
      │                                   │
      └───────────────┬───────────────────┘
                      ▼
               Gunicorn Service
                      │
                   Nginx
                      │
                 Flask Application
                 

---

## Technology Stack

| Technology | Version |
|------------|----------|
| Python | 3.x |
| Flask | Latest |
| Nginx | Latest |
| Jenkins | Latest LTS |
| GitHub Actions | Latest |
| Git | Latest |
| Pytest | Latest |
| Pip | Latest |
| Ubuntu | 22.04 LTS |
---

## Python Repository
https://github.com/GohelG/flask-cicd-app.git

---

## Repository Structure

flask-app/
├── .github/
│ └── workflows/
│ └── ci-cd.yml
├── Jenkinsfile
├── app.py
├── requirements.txt
├── tests/
│ └── test_app.py
├── README.md
└── .gitignore

---

## Branch Structure

main
staging

| Branch | Purpose |
|----------|----------|
| main | Production |
| staging | Testing |

---

## Prerequisites

Install the following software before starting.

- Ubuntu Server
- Nginx
- Git
- Python 3
- pip
- Virtual Environment
- Jenkins
- Java 17
- GitHub Account

---

## Installation Guide

## Install Jenkins

## Update Package Lists

```bash
sudo apt update
```

## Install Required Dependencies

```bash
sudo apt install -y wget curl gnupg
```

## Add Jenkins GPG Key

```bash
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | \
sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
```

## Add Jenkins Repository

```bash
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | \
sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
```

## Install Java

```bash
sudo apt update
sudo apt install -y fontconfig openjdk-17-jre
```

## Install Jenkins

```bash
sudo apt update
sudo apt install -y jenkins
```

## Start Jenkins Service

```bash
sudo systemctl enable jenkins
sudo systemctl start jenkins
sudo systemctl status jenkins
```

## Unlock Jenkins

Open your browser:

http://localhost:8080

Retrieve the initial administrator password:

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

---

## Install Nginx (Reverse Proxy & Web Server)

## Install Nginx

```bash
sudo apt update
sudo apt install -y nginx
```

## Configure Reverse Proxy Server Block

Create a fresh configuration file for the Flask application to route external port `80` traffic to internal Gunicorn port `5000`:
```bash
sudo nano /etc/nginx/sites-available/flask_app
```

Paste the following configurations:
```nginx
server {
    listen 80;
    server_name _; # Replace with domain name or Public IP if available

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static/ {
        alias /var/www/flask-cicd-app/static/;
    }
}
```

## Activate Configuration & Restart Nginx

Enable your proxy block config, remove the default fallback file, and test syntax configurations before initializing the daemon process:
```bash
# Link proxy architecture profile
sudo ln -sf /etc/nginx/sites-available/flask_app /etc/nginx/sites-enabled/

# Remove default server block
sudo rm -f /etc/nginx/sites-enabled/default

# Verify Nginx file integrity 
sudo nginx -t

# Start Engine
sudo systemctl restart nginx
sudo systemctl enable nginx
```

## Configure Workspace Permissions

Ensure Nginx and deployment runners can interact with file directories properly:
```bash
sudo chown -R jenkins:jenkins /var/www/flask-cicd-app
sudo chmod -R 755 /var/www/flask-cicd-app
```

---

## Install Git

## Update Package Lists

```bash
sudo apt update
```

## Install Git

```bash
sudo apt install git -y
```

## Verify Installation

```bash
git --version
```

## Install Latest Git (Optional)

```bash
sudo add-apt-repository ppa:git-core/ppa -y
sudo apt update
sudo apt install git -y
```

## Configure Git

```bash
git config --global user.name "Your Name"

git config --global user.email "youremail@example.com"
```

## Verify Configuration

```bash
git config --global --list
```

---

## Install Python 3

## Update Package Lists

```bash
sudo apt update
```

## Install Python

```bash
sudo apt install python3-full python3-pip python3-venv python3-pytest -y
```

## Create Virtual Environment

```bash
python3 -m venv .venv
```

## Activate Virtual Environment

```bash
source .venv/bin/activate
```

## Install Required Python Packages

```bash
pip install --upgrade pip
pip install pytest gunicorn
```

## Verify Installation

```bash
python3 --version

pip3 --version

pytest --version
```

---

## Install MongoDB 8.x

Official Documentation: <https://www.mongodb.com/docs/v8.0/installation/>

## Check which release of Ubuntu

```bash
cat /etc/lsb-release
```

## Install Dependencies

```bash
sudo apt update
sudo apt install -y gnupg curl
```

## Import MongoDB GPG Key

```bash
curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc | \
sudo gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg --dearmor
```

## Add MongoDB Repository

```bash
echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.2 multiverse" | \
sudo tee /etc/apt/sources.list.d/mongodb-org-8.2.list
```

## Install MongoDB

```bash
sudo apt update
sudo apt install -y mongodb-org
```

## Start MongoDB

```bash
sudo systemctl enable mongod
sudo systemctl start mongod
sudo systemctl status mongod
```

## Verify MongoDB

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

## Checkout

Clone source code from GitHub.

## Build

```bash
python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

## Test

```bash
pytest
```

## Deploy

Deploy to staging server.

Example

```bash
scp -r . jenkins@jenkins-server-public-ip:/var/www/flask-cicd-app
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

http://jenkins-server-public-ip:8080/github-webhook/

Trigger

Push Event

---

## Jenkins Email Notification

Configure SMTP under


Manage Jenkins
↓
Configure System

Example

SMTP Server
smtp.gmail.com
Port
587


Notifications sent for

- Build Success
- Build Failure

---

## GitHub Actions CI/CD Pipeline

## Workflow Location

.github/workflows/ci-cd.yml

---

## Complete GitHub Actions Workflow Code (`ci-cd.yml`)

```yaml
name: Flask Application CI/CD Pipeline

on:
  push:
    branches:
      - staging
    tags:
      - 'v*'
  pull_request:
    branches:
      - staging
      - main

jobs:
  test-and-build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
          pip install pytest mongomock

      - name: Run Unit Tests
        env:
          MONGO_URI: "mongodb://localhost:27017/test_student_db"
          SECRET_KEY: "temporary_github_action_testing_key"
        run: |
          python3 -m pytest -p no:cacheprovider

  deploy-staging:
    needs: test-and-build
    if: github.event_name == 'push' && github.ref == 'refs/heads/staging'
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Deploy Source Code to Staging Environment via SSH
        uses: appleboy/scp-action@master
        with:
          host: \${{ secrets.STAGING_HOST }}
          username: \${{ secrets.STAGING_USER }}
          key: \${{ secrets.STAGING_KEY }}
          source: "."
          target: \${{ secrets.DEPLOY_PATH }}

      - name: Restart Web Services on Staging
        uses: appleboy/ssh-action@master
        with:
          host: \${{ secrets.STAGING_HOST }}
          username: \${{ secrets.STAGING_USER }}
          key: \${{ secrets.STAGING_KEY }}
          script: |
            cd \${{ secrets.DEPLOY_PATH }}
            python3 -m venv venv
            source venv/bin/activate
            pip install -r requirements.txt
            sudo systemctl restart gunicorn

  deploy-production:
    needs: test-and-build
    if: github.event_name == 'push' && startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Deploy Source Code to Production Server
        uses: appleboy/scp-action@master
        with:
          host: \${{ secrets.PRODUCTION_HOST }}
          username: \${{ secrets.PRODUCTION_USER }}
          key: \${{ secrets.PRODUCTION_KEY }}
          source: "."
          target: \${{ secrets.DEPLOY_PATH }}

      - name: Restart Production Web Stack Engine
        uses: appleboy/ssh-action@master
        with:
          host: \${{ secrets.PRODUCTION_HOST }}
          username: \${{ secrets.PRODUCTION_USER }}
          key: \${{ secrets.PRODUCTION_KEY }}
          script: |
            cd \${{ secrets.DEPLOY_PATH }}
            python3 -m venv venv
            source venv/bin/activate
            pip install -r requirements.txt
            sudo systemctl restart gunicorn
```

---

## Workflow Triggers

| Event | Action |
|----------|------------|
| Pull Request | Build & Test |
| Push to staging | Deploy to Staging |
| Release Tag (`v*`) | Deploy to Production |

---

## GitHub Secrets

Go to

Repository
↓
Settings
↓
Secrets and Variables
↓
Actions

Create the following secrets.

| Secret | Description |
|------------|----------------|
| STAGING_HOST | Server IP |
| STAGING_USER | SSH User |
| STAGING_KEY | SSH Private Key |
| PRODUCTION_HOST | Production IP |
| PRODUCTION_USER | Production User |
| PRODUCTION_KEY | Production SSH Key |
| DEPLOY_PATH | Deployment Directory (e.g., /var/www/flask-cicd-app) |

---

## CI/CD Workflow

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

---

## Running Jenkins Pipeline

```bash
git add .
git commit -m "Updated application"
git push origin main
```

---

## Running GitHub Actions Pipeline

Push changes to staging.

```bash
git add .
git commit -m "Testing GitHub Actions"
git push origin staging
```

---

## Production Deployment

Create a release tag.

```bash
git tag v1.0.0
git push origin v1.0.0
```

or publish a GitHub Release.

---

## Author
**Gautam Gohel**
**System Administrator | Cloud Engineer | DevOps Engineer**
