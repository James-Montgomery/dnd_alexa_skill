# Specify the provider and access details
provider "aws" {
  region = "us-east-1"
}

resource "aws_lambda_permission" "dnd_lambda_permission" {
  name = "dnd_lambda_permission"
  statement_id  = "AllowExecutionFromAlexa"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.dnd_lambda.function_name}"
  principal     = "alexa-appkit.amazon.com"
}

resource "aws_lambda_function" "dnd_lambda" {
  name = "dnd_lambda"
  filename         = "lambda_function.zip"
  source_code_hash = "${base64sha256(file("../lambda_code/lambda_function.zip"))}"
  function_name    = "dnd_app"
  role             = "${aws_iam_role.default.arn}"
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.6"
}

resource "aws_iam_role" "dnd_lambda_role" {
  name = "dnd_lambda_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "dnd_lambda_policy" {
  name = "dnd_lambda_policy"
  role = "${aws_iam_role.dnd_lambda_role.id}"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}
