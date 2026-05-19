provider "aws" {
  region                      = "us-east-1"
  access_key                  = "mock_key"
  secret_key                  = "mock_secret"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  # Redirect all AWS service endpoints to Floci
  endpoints {
    s3       = "http://localhost:4566"
    rds      = "http://localhost:4566"
    lambda   = "http://localhost:4566"
    iam      = "http://localhost:4566"
  }
}

# 1. Create 3 S3 Buckets
resource "aws_s3_bucket" "buckets" {
  count  = 3
  bucket = "my-local-bucket-${count.index + 1}"
}

# 2. Create an RDS Database Instance
resource "aws_db_instance" "local_db" {
  allocated_storage   = 10
  engine              = "postgres"
  engine_version      = "15"
  instance_class      = "db.t3.micro"
  db_name             = "local_db"
  username            = "admin"
  password            = "supersecret"
  skip_final_snapshot = true
}

# 3. Packaging and Deploying 2 Lambda Functions
# Package code for Lambda 1
data "archive_file" "lambda_1_zip" {
  type        = "zip"
  output_path = "${path.module}/lambdas/lambda1.zip"
  source {
    content  = "exports.handler = async (event) => { return 'Hello from Lambda 1'; };"
    filename = "index.js"
  }
}

# Package code for Lambda 2
data "archive_file" "lambda_2_zip" {
  type        = "zip"
  output_path = "${path.module}/lambdas/lambda2.zip"
  source {
    content  = "exports.handler = async (event) => { return 'Hello from Lambda 2'; };"
    filename = "index.js"
  }
}

# IAM Role required for Lambda execution
resource "aws_iam_role" "lambda_role" {
  name = "local_lambda_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{ Action = "sts:AssumeRole", Effect = "Allow", Principal = { Service = "lambda.amazonaws.com" } }]
  })
}

resource "aws_lambda_function" "function_1" {
  filename         = data.archive_file.lambda_1_zip.output_path
  function_name    = "my-first-lambda"
  role             = aws_iam_role.lambda_role.arn
  handler          = "index.handler"
  runtime          = "nodejs18.x"
  source_code_hash = data.archive_file.lambda_1_zip.output_base64sha256
}

resource "aws_lambda_function" "function_2" {
  filename         = data.archive_file.lambda_2_zip.output_path
  function_name    = "my-second-lambda"
  role             = aws_iam_role.lambda_role.arn
  handler          = "index.handler"
  runtime          = "nodejs18.x"
  source_code_hash = data.archive_file.lambda_2_zip.output_base64sha256
}
