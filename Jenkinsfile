pipeline {

    agent any

    environment {
        APP_NAME="FlaskApp"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                url: 'https://github.com/<yourusername>/flask-cicd-app.git'
            }
        }

        stage('Build') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                . venv/bin/activate
                pytest
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                chmod +x deploy.sh
                ./deploy.sh
                '''
            }
        }

    }

    post {

        success {
            mail to: 'your@email.com',
                 subject: "SUCCESS: Jenkins Build",
                 body: "Deployment completed successfully."
        }

        failure {
            mail to: 'your@email.com',
                 subject: "FAILED: Jenkins Build",
                 body: "Build failed."
        }

    }

}