import boto3

def build_response(message, session_attributes={}):
    response = {}
    response['version'] = '1.0'
    response['sessionAttributes'] = session_attributes
    response['response'] = message
    return response

def build_SimpleCard(title, body):
    card = {}
    card['type'] = 'Simple'
    card['title'] = title
    card['content'] = body
    return card

def build_PlainSpeech(body):
    speech = {}
    speech['type'] = 'PlainText'
    speech['text'] = body
    return speech

def statement(title, body):
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = True
    return build_response(speechlet)

def lambda_handler(event, context):
    try:
        try:
            intent = event['request']['intent']['name']
        except:
            return 'Successful Test'

        if intent == 'Help':

            help_statement = '''
            Having trouble with Spell Book? Never fear! Spell Book
            is an alexa skill designed to assist dungeon masters to
            quickly reference the 5th edition Dungeons and Dragons
            player's hand book.

            Try asking roll one d Six.

            or

            Open spell book to acid splash.

            '''

            return statement("greeting", help_statement)

        elif intent == 'Inside_Jokes':
            response = '''
            I don't really have one favorite, but Jay ryr and Kate are definitely at the top of my list!
            '''
            return statement("spell", response)

        elif intent == 'Spells':
            spell =  event['request']['intent']['slots']['spell']['value']

            dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
            table = dynamodb.Table('Spell_Book')
            #response = table.scan()

            response = table.get_item(
                Key={
                    'spell_name': spell
                })

            spell_name = response['Item']['spell_name']
            description = response['Item']['description']
            casting_time = response['Item']['casting_time']
            range_ = response['Item']['range']
            components = response['Item']['components']

            response = '''
            {}
            {}
            Casting Time {}
            Range {}
            Components {}
            '''.format(spell_name, description, casting_time, range_, components)

            return statement("spell", response)

        elif intent == 'Dice':
            #results = []
            n = event['request']['intent']['slots']['number']['value']
            v = event['request']['intent']['slots']['value']['value']
            exp = int(round( int(n) * int(v) * .5 + .5, 0 ))
            #for i in range(n):
            #    a = [i+1 for i in range(v)]
            #    x = np.random.choice(a,1)
            #    results.append(results)
            #output = "{}".format(results[0])
            output = "You rolled a cumulative {}".format(exp) #"Numpy not Found"
            return statement("error", output)

    except:
        return statement("error", 'Encountered an error!')
