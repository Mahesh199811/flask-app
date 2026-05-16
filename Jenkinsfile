pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                sh '''
                    rm -rf .git
                    git init
                    git remote add origin https://github.com/Mahesh199811/flask-app.git
                    git fetch --depth 1 origin main
                    git checkout -B main FETCH_HEAD
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t mahesh199811/flask-app:latest .'
            }
        }

        stage('Test') {
            steps {
                sh '''
                    docker run -d --rm -p 9000:9000 \
                                            --name flask-test \
                                            mahesh199811/flask-app:latest
                    sleep 3
                    curl -f http://localhost:9000
                                        docker stop flask-test
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                sh '''
                    echo "$DOCKERHUB_PASSWORD" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin
                    docker push mahesh199811/flask-app:latest
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker stop flask-app-live || true
                    docker rm flask-app-live || true
                    docker pull mahesh199811/flask-app:latest
                    docker run -d \
                      --name flask-app-live \
                      --restart unless-stopped \
                      -p 9000:9000 \
                      mahesh199811/flask-app:latest
                '''
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
            sh 'docker image prune -f'
        }
    }
}
