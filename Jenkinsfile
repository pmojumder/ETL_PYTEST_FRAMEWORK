pipeline {
    agent any

    environment {
        PYTHON_UNBUFFERED = '1'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/pmojumder/ETL_PYTEST_FRAMEWORK.git'
            }
        }

        stage('Setup Environment & Dependencies') {
            steps {
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run PyTest ETL Validations') {
            steps {
                bat '''
                    call venv\\Scripts\\activate
                    pytest --alluredir=allure-results -s || exit 0
                '''
            }
        }
    }

    post {
        always {
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
        }
    }
}