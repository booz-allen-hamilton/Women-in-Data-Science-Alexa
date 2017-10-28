def lambda_handler(event, context):
    if (event["session"]["application"]["applicationId"] !=
          #  "amzn1.echo-sdk-ams.app.bd304b90-xxxx-xxxx-xxxx-xxxxd4772bab"): replace with ours
        raise ValueError("Invalid Application ID")
    
    if event["session"]["new"]:	
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

	### LaunchRequest = what happens when we start the application, 
	### IntentRequest = what happens when someone asks a question
	### SessionEndedRequest = what happens when we end the application
    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])
		
def on_session_started(session_started_request, session):
    print("Starting new session.")

def on_launch(launch_request, session):
    return get_welcome_response()

def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "GetInspirationFig":
        return get_inspiration()
	elif intent_name == "GetMoreInfoOnFig":
		return get_more_info()
	elif intent_name == "GetFieldOfFig":
		return get_field()
	elif intent_name == "GetSpecificFig":
		return 	get_specific_person()
	elif intent_name == "GetExpert":
		return get_expert_in_field()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")
		

def on_session_ended(session_ended_request, session):
    print "Ending session."
    # Cleanup goes here...

def handle_session_end_request():
    card_title = "BAH - Thanks"
    speech_output = ""
    should_end_session = True
	
	return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))
	
def get_welcome_response():
	random_number = get_random_number()
    session_attributes = {}
    card_title = "BAH"
    speech_output = """"Welcome to the Alexa Finding Inspiration Skill. " \
                    "You can ask me who inspires me, or " \
                    "tell me who inspires you."""
    reprompt_text = "Please ask me for who inspires me or , " \
                    "ask me about specific inspirational people."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

		
def get_inspiration():
    session_attributes = {}
    card_title = "Inspiration"
    reprompt_text = ""
    should_end_session = False

	speech_output = "so and so inspires me. "

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
		
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }
