# D&D Alexa Skill

A fun side project to practice developing Alexa Skills by creating an app that provides basic D&D utilities. What is D&D? Dungeons and Dragons is a popular role playing game. It's really fun if you can find the right group, but it has many rules and can be a bit tedious at times.

This app acts as a simple spell book to help any (5th Edition) D&D session go a little bit smoother by quickly reading out the rules for spells.

Much of this guide is based around the [skill-sample-python-fact guide](https://github.com/alexa/skill-sample-python-fact) as of commit bf1bd4e. The alexa skill I will develop here is extremely simple. Follow the official alexa sample skill documentation to create an application leveraging the latest features of the alexa sdk (software development kit).

If you do set up a skill, remember that you can get [paid based on its popularity](https://developer.amazon.com/alexa-skills-kit/rewards)!

## A) Set Up

Before launching the alexa skill, make sure that you have all dependancies installed and properly set up. A complete guide to dependency set up is provided in the [prerequisites file](./prerequisites.md). You will also need an aws (amazon web services) account!

## B) Set Up Skill in the Alexa Developer Console

The first thing we need to do is set up the Alexa skill in the Alexa Developer Console. This will set the scaffold for how users will interact with our skill. Follow this [guide](./guides/Voice_User_Interface.md). During set up you will be asked to set up an "invocation" name. I recommend using something fun like "spell book" or "grimoire". When you are done setting up the interaction model, return to this page.

If you decide to add intents, here is a [guide](https://developer.amazon.com/docs/custom-skills/best-practices-for-sample-utterances-and-custom-slot-type-values.html) for creating sample utterances for those new intents.

## C) Set Up Python Code for Skill

Now that the interaction model is set up we will need to set up the lambda function (sever-less infrastructure) that will act as the backend to our skill. The code is already set up in the `lambda_code` directory. Feel free to look over the code (it's very simple). You should notice that there is a handler for each intent that was set up in the previous set.

To deploy our python code we will need to zip it up:

~~~Bash
cd ./lambda_code
zip -r ./lambda_function.zip ./lambda_function.py
cd ..
~~~

If you had any dependancies that needed to be deployed with the python code you can simply install them into the `lambda_code directory` using something like `pip install -r requirements.txt -t dependancies` and zip them up with the `lambda_function.py` file.

## D) Deploy Cloud Resources Using Terraform

Now we are ready to deploy our lambda into the cloud! This is made very simple using terraform. Simply run the code below:

~~~Bash
cd ./terraform
terraform init
terraform plan
terraform apply -auto-approve
cd ..
~~~

When the lambda deploys it will print an arn onto the console. Keep track of this arn as we will need it in a future step!

### E) Populate DynamoDB Table

Our alexa skill uses a dynamodb table to store all of it's spells. The terraform script created a table for us to use, but it didn't populate the table for us! To populate the table follow the ipython notebook `Populate_Table.ipynb` in the `data` directory.

## F) Link the Front and Back Ends

Finally, you will need to link the front and back ends of the alexa skill. Follow this [guide](./guides/VUI_To_Lambda.md) to do so.

Your Alexa *should* be working now! You can follow these [instructions](./guides/Testing.md) to test your skill's functionality. If you see weird errors (i.e. your invocation calling other skills) to rebuilding your skill. This is a well known [issue](https://forums.developer.amazon.com/questions/180497/alexa-skills-test-mode-not-recognition-invocation.html).

## Acknowledgements

A big thank you to [open5e](https://github.com/eepMoody/open5e). Getting much of this data would have been extremely tedious if not for the efforts of eepMoody in creating open5e. Another big thank you to the publishers of D&D: [Wizards of the Coast](http://company.wizards.com/).

A personal thank you to Jon Rider and Kate Highnam who introduced me to D&D!

## LICENSE

You can find the usage license for this code [here](./LICENSE.md).
