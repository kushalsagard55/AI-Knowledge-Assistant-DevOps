pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install CPU PyTorch') {
            steps {
                sh '''
                    python3 -m pip install --break-system-packages \
                    torch \
                    --index-url https://download.pytorch.org/whl/cpu
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m pip install --user \
                    --break-system-packages \
                    -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    export APP_NAME="AI Knowledge Assistant"
                    export APP_VERSION="1.0.0"
                    export OPENAI_API_KEY="test-key"
                    export GEMINI_API_KEY="test-key"
                    export GEMINI_MODEL="models/gemini-3.5-flash"
                    export MONGODB_URL="mongodb://localhost:27017"
                    export DATABASE_NAME="ai_knowledge_assistant"
                    export JWT_SECRET_KEY="test-secret"
                    export JWT_ALGORITHM="HS256"
                    export ACCESS_TOKEN_EXPIRE_MINUTES="30"

                    python3 -m pytest -v
                '''
            }
        }
        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ai-knowledge-assistant:latest .
                '''
            }
        }
    }

    post {
        success {
            echo 'CI Pipeline completed successfully!'
        }

        failure {
            echo 'CI Pipeline failed. Check the console output.'
        }
    }
}