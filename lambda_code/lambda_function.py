import boto3
import logging

def build_response(message, session_attributes={}):
    response = {}
    response["version"] = "1.0"
    response["sessionAttributes"] = session_attributes
    response["response"] = message
    return response

def build_SimpleCard(title, body):
    card = {}
    card["type"] = "Simple"
    card["title"] = title
    card["content"] = body
    return card

def build_PlainSpeech(body):
    speech = {}
    speech["type"] = "PlainText"
    speech["text"] = body
    return speech

def statement(title, body):
    speechlet = {}
    speechlet["outputSpeech"] = build_PlainSpeech(body)
    speechlet["card"] = build_SimpleCard(title, body)
    speechlet["shouldEndSession"] = True
    return build_response(speechlet)

def retrieve_spell(spell):
    # open connection to table
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table = dynamodb.Table("Spell_Book")
    # query table for spell
    query_response = table.get_item(Key={"spell_name": spell})["Item"]
    # parse response
    spell_name = query_response["spell_name"]
    description = query_response["description"]
    casting_time = query_response["casting_time"]
    range_ = query_response["range"]
    components = query_response["components"]
    # create response
    response = """
    {} \n{} \nCasting Time {} \nRange {} \nComponents {}
    """.format(spell_name, description, casting_time, range_, components)
    return response

def lambda_handler(event, context):

    logging.info("Call Made.")
    logging.debug("Event: {}".format(event))
    logging.debug("Context: {}".format(context))

    try:
        intent = event["request"]["intent"]["name"]
    except Exception as e:
        logging.error("Error Getting Intent:\n{}".format(e))
        title = "intent_not_found"
        response = "Encountered an error!"
        logging.info("Returning Response.")
        return statement(title, response)

    try:
        if intent == "Help":
            logging.info("Help Intent")
            title = "help_response"
            response = "Get Help."

        elif intent == "Inside_Jokes":
            logging.info("Inside Joke Intent")
            title = "inside_joke_response"
            response = """
            I don't really have one favorite, but Jay Rye and Kate are definitely at the top of my list!
            """

        elif intent == "Spells":
            logging.info("Spells Intent")
            spell =  event["request"]["intent"]["slots"]["spell"]["value"]
            logging.info("".format(spell))
            title = "spell_response"
            response = retrieve_spell(spell)

        else:
            logging.error("Unexpected Intent: {}".format(intent))
            title = "unexpected_intent_response"
            response = "Encountered an Error!"

    except Exception as e:
            logging.error("Unexpected Error:\n{}".format(e))
            title = "error_response"
            response = "Encountered an error!"

    logging.info("Returning Response.")
    return statement(title, response)
