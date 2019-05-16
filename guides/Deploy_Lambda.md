
~~~
cd ./lambda_code
#mkdir skill_env
#pip install -r requirements.txt -t skill_env
#cp -r ./lambda_function.py ./skill_env/
#zip -r ./lambda_function.zip ./skill_env/*
zip -r ./lambda_function.zip ./lambda_function.py
~~~

~~~
rm -r ./skill_env
rm ./lambda_function.zip
~~~

~~~
terraform init
~~~

~~~
terraform build .
~~~
