pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/your-repo/aws-data-pipeline.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build('data-pipeline:latest')
                }
            }
        }
        stage('Push to ECR') {
            steps {
                script {
                    docker.withRegistry('https://aws_account_id.dkr.ecr.region.amazonaws.com', 'ecr:aws') {
                        docker.image('data-pipeline:latest').push('latest')
                    }
                }
            }
        }
        stage('Deploy with Terraform') {
            steps {
                script {
                    sh 'terraform init'
                    sh 'terraform apply -auto-approve'
                }
            }
        }
        stage('Test Lambda Function') {
            steps {
                script {
                    sh '''
                    aws lambda invoke --function-name data_pipeline out.txt
                    cat out.txt
                    '''
                }
            }
        }
    }
}
