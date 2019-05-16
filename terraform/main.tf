# Specify the provider and access details
provider "aws" {
  region = "us-east-1"
}

resource "aws_lambda_permission" "dnd_lambda_permission" {

  statement_id  = "AllowExecutionFromAlexa"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.dnd_lambda.function_name}"
  principal     = "alexa-appkit.amazon.com"
}

resource "aws_lambda_function" "dnd_lambda" {

  filename         = "../lambda_code/lambda_function.zip"
  source_code_hash = "${base64sha256(file("../lambda_code/lambda_function.zip"))}"
  function_name    = "Spell_Book"
  role             = "${aws_iam_role.dnd_lambda_role.arn}"
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

resource "aws_iam_role_policy" "dnd_dynamodb_lambda_policy"{
  name = "dnd_dynamodb_lambda_policy"
  role = "${aws_iam_role.dnd_lambda_role.id}"
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:*"
      ],
      "Resource": "${aws_dynamodb_table.spell_book.arn}"
    }
  ]
}
EOF
}

resource "aws_dynamodb_table" "spell_book" {
  name           = "Spell_Book"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "spell_name"

  attribute {
    name = "spell_name"
    type = "S"
  }

}
