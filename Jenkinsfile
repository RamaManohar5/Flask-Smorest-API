pipeline {
    environment {
        registry = "ramamanohark555/flask_restful_api_repo"
        registryCredential = 'dockerhub_credentials_token'
        dockerImage = 'flask=smorest-api'
    }

    agent any

    stages {
        stage('Cloning our Git') {
            steps {
                git 'https://github.com/RamaManohar5/Flask-Smorest-API.git'
            }
        }
        stage('Building our image') {
            steps{
                script {
                    dockerImage = docker.build registry + ":$BUILD_NUMBER"
                }
            }
        }
        stage('Deploy our image') {
            steps{
                script {
                    docker.withRegistry( '', registryCredential ) {
                        dockerImage.push()
                    }
                }
            }
        }
        stage('Cleaning up') {
            steps{
                sh "docker rmi $registry:$BUILD_NUMBER"
            }
        }
    }
}