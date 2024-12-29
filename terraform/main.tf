provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "data_bucket" {
  bucket = "your-data-bucket-name"
}

resource "aws_rds_instance" "database" {
  allocated_storage    = 10
  engine               = "mysql"
  engine_version       = "8.0"
  instance_class       = "db.t2.micro"
  name                 = "mydatabase"
  username             = "admin"
  password             = "password"
  parameter_group_name = "default.mysql8.0"
  skip_final_snapshot  = true
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Sid    = "",
        Principal = {
          Service = "lambda.amazonaws.com",
        },
      },
    ],
  })
}

resource "aws_lambda_function" "data_pipeline" {
  function_name = "data_pipeline"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.handler"
  runtime       = "python3.9"

  image_uri = aws_ecr_repository.repo.repository_url

  environment {
    variables = {
      S3_BUCKET     = "your-data-bucket-name"
      S3_KEY        = "path/to/your/file"
      RDS_ENDPOINT  = aws_rds_instance.database.endpoint
      RDS_USER      = "admin"
      RDS_PASSWORD  = "password"
      RDS_DB        = "mydatabase"
      GLUE_DATABASE = "your-glue-database"
      GLUE_TABLE    = "your-glue-table"
    }
  }
}

resource "aws_ecr_repository" "repo" {
  name = "data-pipeline-repo"
}

output "lambda_function_name" {
  value = aws_lambda_function.data_pipeline.function_name
}
