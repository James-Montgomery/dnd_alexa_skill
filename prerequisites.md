## Set Up

Before launching the Alexa Skill, make sure that you have these dependancies installed and properly set up.

Overview:
1. Python
2. Terraform
3. AWS CLI Tools

### 1) Python

If you want to test code locally before deploying, you will need python. I recommend using the Anaconda distribution of python. In addition to Pypi's `pip`, Anaconda comes with it's own package manager / virtual environment manager `conda`.

Follow the instructions here: [Install Python](https://docs.anaconda.com/anaconda/install/)

### 2) Terraform

We will use terraform to deploy the actual infrastructure in aws. I recommend [brew](https://brew.sh/) installing.

~~~Bash
brew install terraform
~~~

Verify installation by running:

~~~Bash
terraform
~~~

Rather than hard coding aws credentials into a terraform file, I recommend making them environment credentials. Replace `XXX` with your actual credentials.

~~~Bash
"# AWS Credentials" >> ~/.bash_profile
"export AWS_ACCESS_KEY_ID=\"XXX\"" >> ~/.bash_profile
"export AWS_SECRET_ACCESS_KEY=\"XXX\"" >> ~/.bash_profile
source ~/.bash_profile
~~~

Check that you can access these environment variables:

~~~Bash
echo $AWS_ACCESS_KEY_ID
echo $AWS_SECRET_ACCESS_KEY
~~~

Your credentials should print out in the terminal. Storing important credentials in plain text is not always the best idea. I would use credentials for a user with limited powers. You can create such users using aws IAM. You could also store such credentials in a Vault or protected server for increased security.

### 3) AWS CLI Tool

It can also be useful to have the aws cli tool on hand. I wish all of the cloud infrastructure work could be done by terraform alone, but there are some quirks about creating ami's using terraform that make it more convenient to use the aws cli tool.

The aws cli tool is also useful for programmatically grabbing the s3 prefixes of all of the aws regions which may me necessary if you plan to run this script in a region other than `us-east-1`.

~~~Bash
pip install awscli==1.16.112
~~~

We can set a default profile using the code below. We already set the key and secret in the terraform step. You can also set a default region here.

~~~Bash
aws config
~~~
