pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'Flask-Smorest-API'
        DOCKERHUB_CREDENTIALS = credentials('dockerhub_token')
        DOCKERHUB_REPO = 'ramamanohark555/flask-smorest-api'
    }
    
    stages {
        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: DOCKERHUB_CREDENTIALS, usernameVariable: 'DOCKERHUB_CREDENTIALS_USR', passwordVariable: 'DOCKERHUB_CREDENTIALS_PSW')]) {
                    sh "docker login -u $DOCKERHUB_CREDENTIALS_USR -p $DOCKERHUB_CREDENTIALS_PSW"
                }
            }
        }
        
        stage('Clean Up Existing Docker Resources') {
            steps {
                script {
                    echo 'Cleaning up existing Docker containers and images...'
                    sh """
                        docker ps -a --filter "ancestor=${DOCKER_IMAGE}" --format "{{.ID}}" | xargs -r docker rm -f
                        docker ps -a --filter "name=${DOCKER_IMAGE}_container" --format "{{.ID}}" | xargs -r docker rm -f
                        docker rmi -f ${DOCKER_IMAGE} || true
                        docker rmi -f ${DOCKERHUB_REPO} || true
                    """
                }
            }
        }
        
        stage('Build and Push Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    sh "docker build -t ${DOCKER_IMAGE} ."
                    echo 'Tagging Docker image...'
                    sh "docker tag ${DOCKER_IMAGE} ${DOCKERHUB_REPO}"
                    echo 'Pushing Docker image to Docker Hub...'
                    sh "docker push ${DOCKERHUB_REPO}"
                    sh 'docker images'
                }
            }
        }
        
        stage('Run Docker Container') {
            steps {
                script {
                    echo 'Running Docker container...'
                    try {
                        sh "docker run -d -p 8000:8000 --name ${DOCKER_IMAGE}_container ${DOCKERHUB_REPO}"
                    } catch (Exception e) {
                        echo 'Failed to run Docker container'
                        sh "docker logs ${DOCKER_IMAGE}_container || true"
                        throw e
                    }
                }
            }
        }
        
        stage('Check Running Containers') {
            steps {
                script {
                    echo 'Checking running containers...'
                    sh "docker ps"
                }
            }
        }
        
        stage('Check Container Logs') {
            steps {
                script {
                    echo 'Checking container logs...'
                    sh "docker logs ${DOCKER_IMAGE}_container || true"
                }
            }
        }
    }
    
    post {
        always {
            script {
                echo 'Performing cleanup...'
                sh """
                    docker rm -f ${DOCKER_IMAGE}_container || true
                    docker rmi -f ${DOCKER_IMAGE} || true
                """
            }
        }
        
        success {
            echo 'Pipeline completed successfully.'
        }
        
        failure {
            echo 'Pipeline failed.'
        }
    }
}
