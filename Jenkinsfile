pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'mayur2808/myweb'
        DOCKER_CREDENTIALS = credentials('dockerhub-creds')
        SSH_KEY = 'ec2-ssh-key'
        VERSION_FILE = 'build_version.txt'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Mayur2801/web-login'
            }
        }

        stage('Set Version') {
            steps {
                script {
                    if (!fileExists(env.VERSION_FILE)) {
                        writeFile file: env.VERSION_FILE, text: '1'
                        env.APP_VERSION = 'v1'
                    } else {
                        def currentVersion = readFile(env.VERSION_FILE).trim().toInteger()
                        def newVersion = currentVersion + 1
                        writeFile file: env.VERSION_FILE, text: newVersion.toString()
                        env.APP_VERSION = "v${newVersion}"
                    }
                    echo "App Version: ${env.APP_VERSION}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE:$APP_VERSION .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push $DOCKER_IMAGE:$APP_VERSION
                    '''
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent([SSH_KEY]) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ec2-user@ec2-44-203-74-121.compute-1.amazonaws.com <<EOF
                        if ! command -v docker &> /dev/null; then
                            echo "Installing Docker..."
                            sudo yum update -y
                            sudo yum install -y docker
                            sudo systemctl start docker
                            sudo systemctl enable docker
                            sudo usermod -aG docker ec2-user
                        fi

                        sudo docker pull $DOCKER_IMAGE:$APP_VERSION
                        sudo docker stop myweb || true
                        sudo docker rm myweb || true
                        sudo docker run -d --name myweb -p 80:80 $DOCKER_IMAGE:$APP_VERSION
EOF
                    """
                }
            }
        }
    }

    post {
        success {
            archiveArtifacts artifacts: 'build_version.txt', onlyIfSuccessful: true
        }
    }
}
