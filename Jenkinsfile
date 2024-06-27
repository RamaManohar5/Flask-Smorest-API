pipeline {
    agent any
    
    // Environment setup
    environment {
        registryCredential = 'dockerhub_credentials_token' // Jenkins Credentials ID for Docker Hub
        dockerImage = "my-image:latest"
        dockerRegistry = "docker.io" // Docker registry hostname (e.g., Docker Hub)
        dockerHost = "tcp://docker-host:2376" // Docker host URL (if using a remote Docker host)
        githubCredentials = 'github_credentials_token' // Jenkins Credentials ID for GitHub
    }
    
    // Stages
    stages {
        stage("Clone Repository") {
            steps {
                // Checkout your private GitHub repository using Jenkins credentials
                git credentialsId: githubCredentials, url: 'https://github.com/RamaManohar5/Flask-Smorest-API.git', branch: 'main'
            }
        }
        
        stage("Build Docker Image") {
            steps {
                script {
                    // Build Docker image using Dockerfile in the repository
                    docker.build("${dockerRegistry}/${dockerImage}")
                }
            }
        }
        
        stage("Push Docker Image") {
            steps {
                script {
                    // Authenticate with Docker registry
                    docker.withRegistry("${dockerRegistry}", "${registryCredential}") {
                        // Push Docker image to registry
                        dockerImage.push()
                    }
                }
            }
        }
    }
    
    // Post-build actions
    post {
        success {
            echo 'Deployment successful!'
        }
        failure {
            echo 'Deployment failed!'
        }
    }
}
