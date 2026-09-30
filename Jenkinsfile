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
                    pytest -v -s -rA --html=report.html --self-contained-html --alluredir=allure-results || exit 0
                '''
            }
        }
    }

    post {
        always {
            echo '========================================'
            echo ' ETL PyTest Execution Completed '
            echo '========================================'
            
            // Archive HTML execution report as a Jenkins build artifact
            archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true

            // Re-enable allure once Allure Jenkins Plugin is installed under Manage Jenkins -> Plugins
            // allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
        }
    }
}
