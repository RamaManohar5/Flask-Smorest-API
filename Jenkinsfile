pipeline {
    agent any
    
    // Environment setup
    environment {
        registryCredential = 'dockerhub_credentials_token' // Jenkins Credentials ID for Docker Hub
        dockerImage = "Flask-Smorest-API:latest"
        dockerRegistry = 'docker.io' // Docker registry hostname (e.g., Docker Hub)
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
        
        stage("Docker Login") {
            steps {
                script {
                    // Login to Docker registry
                    docker.withRegistry("${dockerRegistry}", "${registryCredential}") {
                        // Perform Docker login
                        docker.login()
                    }
                }
            }
        }
        
        stage("Build Docker Image") {
            steps {
                script {
                    // Build Docker image using Dockerfile in the repository
                    def dockerImageTag = "${dockerRegistry}/${dockerImage}"
                    docker.build(dockerImageTag)
                }
            }
        }
        
        stage("Push Docker Image") {
            steps {
                script {
                    // Push Docker image to registry
                    def dockerImageTag = "${dockerRegistry}/${dockerImage}"
                    docker.withRegistry("${dockerRegistry}", "${registryCredential}") {
                        dockerImage.push()
                    }
                }
            }
        }
        
        stage("Docker Logout") {
            steps {
                script {
                    // Logout from Docker registry
                    docker.withRegistry("${dockerRegistry}", "${registryCredential}") {
                        docker.logout()
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
