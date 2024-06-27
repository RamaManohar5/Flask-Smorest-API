pipeline {
    agent any

    environment {
        registry = "ramamanohark555/flask_restful_api_repo"
        registryCredential = 'dockerhub_credentials_token'
        dockerImage = 'flask-smorest-api'
        githubCredentials = 'github_credentials_token'
    }

    stages {
        stage('Cloning Git Repository') {
            steps {
                git credentialsId: githubCredentials, url: "https://github.com/RamaManohar5/Flask-Smorest-API.git", branch: 'main'
                echo 'Git Checkout Completed'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker image with the appropriate tag
                    // sh "docker build -t ${registry}:${BUILD_NUMBER} ."
                    sh "docker build --no-cache -t ${registry} ."
                    echo 'Build Image Completed'
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                // Login to Docker Hub using credentials
                withCredentials([usernamePassword(credentialsId: 'dockerhub_credentials_token', usernameVariable: 'DOCKERHUB_CREDENTIALS_USR', passwordVariable: 'DOCKERHUB_CREDENTIALS_PSW')]) {
                    sh "echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin"
                    echo 'Login Completed'
                }
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                script {
                    // Push Docker image to Docker Hub
                    sh "docker push ${registry} "
                    echo 'Push Image Completed'
                }
            }
        }
    }

    post {
        always {
            // Always perform Docker logout after the pipeline completes
            sh 'docker logout'
        }
    }
}
