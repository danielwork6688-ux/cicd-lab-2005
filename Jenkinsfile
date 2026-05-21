pipeline {
    agent any

    environment {
        DOCKER_IMAGE   = "danielwork6688/django-todo-app"
        ANSIBLE_SERVER = "20.195.40.198"
        ANSIBLE_USER   = "azureuser"
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

        stage('CD: Deploy via Ansible') {
            steps {
                sshagent(['ansible-ssh-key']) {
                    sh """
                        scp -o StrictHostKeyChecking=no -r ansible/ ${ANSIBLE_USER}@${ANSIBLE_SERVER}:~/ansible/

                        ssh -o StrictHostKeyChecking=no ${ANSIBLE_USER}@${ANSIBLE_SERVER} '
                            cd ~/ansible
                            ansible-playbook playbooks/deploy.yml
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