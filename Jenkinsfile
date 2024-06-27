pipeline {
    agent any

    environment {
        registry = "ramamanohark555/flask_restful_api_repo"
        registryCredential = 'dockerhub_credentials_token'
        dockerImage = 'flask=smorest-api'
        githubCredentials = 'github_credentials_token'
    }

    stages {
        stage('Cloning our Git') {
            steps {
                git credentialsId: githubCredentials, url: "https://github.com/RamaManohar5/Flask-Smorest-API.git", branch: 'main'
                echo 'Git Checkout Completed'
            }
        }
    }
}
