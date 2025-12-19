pipeline {
    agent any

    triggers {
        cron('H 10 * * *')   // Daily run around 10 AM
    }

    environment {
        VENV = ".venv"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                bat '''
                python -m venv %VENV%
                call %VENV%\\Scripts\\activate
                pip install --upgrade pip
                pip install -r requirements.txt
                python -m playwright install
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                call %VENV%\\Scripts\\activate
                pytest
                '''
            }
        }
    }

    post {
        always {
            allure(
                includeProperties: false,
                results: [[path: 'reports/allure-results']]
            )
        }

        failure {
            echo '❌ Test execution failed'
        }

        success {
            echo '✅ Test execution successful'
        }
    }
}
