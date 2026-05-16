pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "mahesh199811/flask-app"
        DOCKER_TAG   = "${BUILD_NUMBER}"
        CONTAINER_NAME = "flask-app-live"
    }

    stages {

        stage('Checkout') {
            steps {
                // Pull code from GitHub
                git branch: 'main',
                    url: 'https://github.com/Mahesh199811/flask-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    // Run container and check it responds
                    sh """
                        docker run -d --rm -p 9000:9000 \
                          --name flask-test-${BUILD_NUMBER} \
                          ${DOCKER_IMAGE}:${DOCKER_TAG}
                        sleep 3
                        curl -f http://localhost:9000 || exit 1
                        docker stop flask-test-${BUILD_NUMBER}
                    """
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('', 'dockerhub-creds') {
                        docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push()
                        docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push('latest')
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    sh """
                        docker stop ${CONTAINER_NAME} || true
                        docker rm   ${CONTAINER_NAME} || true
                        docker pull ${DOCKER_IMAGE}:latest
                        docker run -d \
                          --name ${CONTAINER_NAME} \
                          --restart unless-stopped \
                                                    -p 9000:9000 \
                          ${DOCKER_IMAGE}:latest
                    """
                }
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline succeeded! App is live.'
        }
        failure {
            echo '❌ Pipeline failed. Check logs above.'
        }
        always {
            // Clean up dangling images to save disk
            sh 'docker image prune -f'
        }
    }
}
