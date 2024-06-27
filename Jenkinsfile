pipeline{
    agent any

    // environment setup
    environment{
        registryCredential = 'dockerhub_credentials_token' //Jenkins Credentials for Docker 
        dockerImage = "my-image:latest"
        dockerRegistry = "docker.io" // Docker registry hostname (e.g., Docker Hub)
        dockerHost = "tcp://docker-host:2376" // Docker host URL (if using a remote Docker host)
    }

    // staging 
    stages{
        stage("Clone Repository"){
            steps{
                // checkout git repository
                git 'https://github.com/RamaManohar5/Flask-Smorest-API.git'
                // Checkout your private GitHub repository using Jenkins credentials
                // git credentialsId: 'your-github-credentials-id', url: 'https://github.com/RamaManohar5/Flask-Smorest-API.git'
            }
        }

        stage("Build Docker Image"){
            steps{
                script{
                    // build docker image using Dockerfile in the repository
                    docker.build(${dockerRegistry}/${dockerImage})
                }
            }
        }

        stage("Push Docker Image"){
            steps{
                script{
                    // authenticate the registry
                    docker.withRegistry(${dockerRegistry}, ${registryCredential})
                    // push to the docker
                    dockerImage.push()
                }
            }
        }
    }
}