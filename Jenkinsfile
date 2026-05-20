pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "danielwork6688/django-todo-app"
        APP_SERVER   = "4.194.234.196"
        APP_USER     = "azureuser"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('CI: Build Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE:$BUILD_NUMBER .'
            }
        }

        stage('CI: Run Tests') {
            steps {
                sh '''
                    docker run --rm $DOCKER_IMAGE:$BUILD_NUMBER \
                        python manage.py test --verbosity=2
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker tag $DOCKER_IMAGE:$BUILD_NUMBER $DOCKER_IMAGE:latest
                        docker push $DOCKER_IMAGE:$BUILD_NUMBER
                        docker push $DOCKER_IMAGE:latest
                    '''
                }
            }
        }

stage('CD: Deploy to App Server') {
    steps {
        sshagent(['appserver-ssh-key']) {
            sh """
                ssh -o StrictHostKeyChecking=no ${APP_USER}@${APP_SERVER} '
                    docker pull danielwork6688/django-todo-app:latest

                    docker stop todo-app 2>/dev/null || true
                    docker rm todo-app 2>/dev/null || true

                    docker run -d \
                        --name todo-app \
                        --restart unless-stopped \
                        -p 127.0.0.1:8000:8000 \
                        danielwork6688/django-todo-app:latest

                    docker image prune -f
                    echo Deploy xong!
                '
            """
        }
    }
}
    }

    post {
        success {
            echo '✅ Pipeline thành công!'
        }
        failure {
            echo '❌ Pipeline thất bại!'
        }
        always {
            sh 'docker logout || true'
            sh 'docker image prune -f || true'
        }
    }
}