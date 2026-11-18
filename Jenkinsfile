
pipeline {
    agent any

    environment {
        PATH = "/snap/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
        IMAGE_NAME = "vishal249/secure-devops-app"
    }

    options {
        timestamps()
    }

    stages {
        stage('Test Application') {
            steps {
                sh '''
                    python3 -m venv .venv-ci
                    .venv-ci/bin/python -m pip install -r requirements.txt
                    .venv-ci/bin/python -m pip install pytest
                    .venv-ci/bin/python -m pytest -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t $IMAGE_NAME:$BUILD_NUMBER .
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        set +x
                        echo "$DOCKER_PASS" | docker login \
                            -u "$DOCKER_USER" --password-stdin
                        docker push $IMAGE_NAME:$BUILD_NUMBER
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Staging') {
            steps {
                sh '''
                    kubectl apply -f k8s/staging-deployment.yaml
                    kubectl apply -f k8s/staging-service.yaml
                    kubectl set image deployment/secure-devops-app \
                        flask-app=$IMAGE_NAME:$BUILD_NUMBER -n staging
                    kubectl rollout status deployment/secure-devops-app \
                        -n staging --timeout=120s
                '''
            }
        }

        stage('Approve Production') {
            steps {
                input message: 'Approve deployment to production?',
                      ok: 'Deploy to Production'
            }
        }

        stage('Deploy to Production') {
            steps {
                sh '''
                    kubectl apply -f k8s/production-deployment.yaml
                    kubectl set image deployment/secure-devops-app \
                        flask-app=$IMAGE_NAME:$BUILD_NUMBER -n production
                    kubectl rollout status deployment/secure-devops-app \
                        -n production --timeout=120s
                '''
            }
        }
    }
}
