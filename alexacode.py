try:
    import numpy as np
    import random
    import pandas as pd
    import gspread 
    from oauth2client.service_account import ServiceAccountCredentials
    import json
    import re
    
    import urllib
    from bs4 import BeautifulSoup 
except:
    print("Problem importing libraries")






listversion = [['Marie Curie',
  'She is a polish-born French physicist and chemist best known for her contributions to radioactivity.',
  'https://en.wikipedia.org/wiki/Marie_Curie',
  None,
  None,
  'Science'],
 ['Hillary Manson',
  'She is the Founder of Fast Forward Labs, a machine intelligence research company, and the Data Scientist in Residence at Accel.',
  'https://en.wikipedia.org/wiki/Hilary_Mason_(data_scientist)',
  '@hmason',
  None,
  'Data Science'],
 ['Maryam Mirzakhani',
  'She is the first woman to win the Fields Medal, the mathematics equivalent of the Nobel Prize, for her work in theoretical mathematics.',
  'https://en.wikipedia.org/wiki/Maryam_Mirzakhani',
  None,
  None,
  'Mathematics'],
 ['Ada Lovelace',
  'She is known for her work on the Analytical Engine, a proposed mechanical general-purpose computer and is recognized for creating the first algorithm\xa0and as the first computer programmer because of this work. ',
  'https://en.wikipedia.org/wiki/Ada_Lovelace',
  None,
  None,
  'Mathematics'],
 ['Grace Hopper',
  'She was a groundbreaking computer scientist and a lifelong member of the military',
  'https://en.wikipedia.org/wiki/Grace_Hopper',
  None,
  None,
  'Computer Science'],
 ['Hillary Clinton',
  "She is an American politician who was the First Lady of the United States from 1993 to 2001, U.S. Senator from New York from 2001 to 2009, 67th United States Secretary of State from 2009 to 2013, and the Democratic Party's nominee for President of the United States in the 2016 election.",
  'https://en.wikipedia.org/wiki/Hillary_Clinton',
  '@HillaryClinton',
  None,
  'Politics'],
 ['Michelle Obama',
  'She is an American lawyer and writer who was First Lady of the United States from 2009 to 2017.',
  'https://en.wikipedia.org/wiki/Michelle_Obama',
  '@MichelleObama',
  None,
  'Politics'],
 ['Amelia Earhart',
  'She was an American aviation pioneer and author. She is known for setting many early aviation records, including being the first woman to fly solo across the Atlantic Ocean.',
  'https://en.wikipedia.org/wiki/Amelia_Earhart',
  None,
  None,
  'Aviation'],
 ['Ching Shih',
  'She was a prominent pirate in middle Qing China, who terrorized the China Sea in the early 19th century. She was one of the few pirate captains to retire from piracy and is considered to be the most successful pirate in history.',
  'https://en.wikipedia.org/wiki/Ching_Shih',
  None,
  None,
  'Piracy'],
 ['Billie Jean King',
  'She is an American former World No. 1 professional tennis player who won 39 Grand Slam titles.',
  'https://en.wikipedia.org/wiki/Billie_Jean_King',
  None,
  None,
  'Sports'],
 ['Benazir Bhutto',
  "She was the 11th Prime Minister of Pakistan (1993-1996) and the first woman to head a Muslim state. During her leadership, she ended military dictatorship in her country and fought for women's rights.",
  'https://en.wikipedia.org/wiki/Benazir_Bhutto',
  None,
  None,
  'Politics'],
 ['Mary Anning',
  'She was an English fossil collector, dealer, and paleontologist who became known around the world for important finds she made in Jurassic marine fossil beds in the cliffs along the English Channel.',
  'https://en.wikipedia.org/wiki/Mary_Anning',
  None,
  None,
  'Science'],
 ['Oprah Winfrey',
  'She is an American media proprietor, talk show host, actress, producer, and philanthropist',
  'https://en.wikipedia.org/wiki/Oprah_Winfrey',
  '@Oprah',
  None,
  'Media'],
 ['Rachel Maddow',
  'She is an American television host, political commentator, and author. ',
  'https://en.wikipedia.org/wiki/Rachel_Maddow',
  '@Maddow',
  None,
  'Media'],
 ['Diana, Princess of Wales ',
  'She was well-known for her global humanitarian efforts.',
  'https://en.wikipedia.org/wiki/Diana,_Princess_of_Wales',
  None,
  None,
  'Humanitarianism'],
 ['Malala Yousafzai',
  ' Young pakistani activist for female education and development',
  'https://en.wikipedia.org/wiki/Malala_Yousafzai',
  None,
  None,
  'Humanitarianism'],
 ['Zoella Sugg',
  'She is an English fashion and beauty vlogger, YouTuber, and author. She is best known by her YouTube username Zoella.',
  'https://en.wikipedia.org/wiki/Zoella',
  '@Zoella',
  '@Zoella',
  'Beauty'],
 ['Beyoncé Giselle Knowles-Carter',
  'Dedicated to what she does and extremely successful at it, she knows how to carry herself and have her voice heard',
  'https://en.wikipedia.org/wiki/Beyoncé',
  '@Beyonce',
  None,
  'Artist']]
 
 
pd.set_option('display.max_colwidth', -1)

inspirationDF =  pd.DataFrame(listversion)

#x = inspirationDF.to_json() #from DF to JSON
#y = pd.read_json(x) #from JSON to DF


  

def getGoogleSheet():
    data= {}
    data ["type"]= "service_account"
    data ["project_id"] = "wids-alexa"
    data ["private_key_id"]= "2447ca9ee70f02caf69786ffc1bb4f09652e7a05"
    data ["private_key"]= "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDRKWvoRoHDy1s6\nQJQ4mWTXFkc5i2iotZOg8jGzUZ+Yyt6zZpFFQ8iLCgQOsDOq8FxgP/B4zhrGGYl2\nhtTujPazIRZJCu5aa1I1ezmNv0zAHOAa4VtWvkgAM5bkFEtiBKRs5cHdYIxKfAQ0\nIgNlIb0R113Duct1yjSMEk1WGgl8/57a83PUahkqzQMQROgiL/2oYCKaxYmjrBex\nJUfU1J9I+GC4qFHcRNcbnwo/9vJdaP5lt67DztZmorOUyYJPB3P8r3DRJKcdPPK0\nnMQJB47ebXEZORp6ESWWASAdqEcZvRFIo+S5RnR4AGrwAQWls2LAkJIReFli3op4\nkASB0eyxAgMBAAECggEACizzX058JlQGBn8jzDPHkHXjVdeuv3PDUIjX2tB1bOUv\nERfuqKmpNP0cwMDZEqTflEh9YMiDdvBrxpoSpomxwCSI8AQZynOpgTPofePjo6kD\n92rP8G1mFVRtL9Vo7BuBCvyL15hIhaB47TcGZpd4mkiZpYRWyKPjYI53Yrag5YrM\nxeyw5OefS7AzBcMRKeMan2GrPMH2ybvb3+ZEypT+ZOhrvsEFtUyUPAiQkUwVnRL4\nCvTvpDzu9Y1kHRZarjHt/itoLiiRi1nXj+RPZG2USn5TLQgpZpSFwmwUkfESgtL/\nG20Y6LTihLCU46yMtvGfmoZnGNA/Ex8BZ76IXQFRkQKBgQD/cKgn87bWfKlP2OdB\nZPIJhLVF+QCI8OctKTY+p3SyDo2lKsQQlE7QGQs1oFYbr5WIdhMeu6/YDR/hGx/H\nSBTkavMgvLFQ+O/MBUB1rXhBu67Dxf30R7jAs3inRLvfTstFGZX836QRQhqPerzv\nQW81wOuxT9ZTTQZxByi1vE/N9QKBgQDRnsuJ17gyHXBgRuieBIwXUnRmg4la3VNw\nvw57XZFPAYEU9aYEjdHFw2BeQaIoPmLvNfsfqVRYerleJWzVc++g4LYn3IG0u6z5\nXiQvd0oxG5N6tkkBTzrmPa2fF3kz2gaLnwvYPE3LYmYXfxtSMmd161RZEjFGZaYP\nv2ZIMqbSTQKBgERyUozKEG8u3kuICoeKXhTQ26YRT+Rh8QA379IgGvPvVGMyr3Dl\n3KyEWW2YNhqbFQ2I3hy5HChfc/BkzUIf/YEra1SVW0ogOllH+vrNbdDnUrAg6KjB\nYy83qBfiIhl3Sp6MeZVV8+ev9+AEeoX92afktwM/KmYN2LEGwxDXkebVAoGBAIAZ\nnKUGMUhe+Te83ZcDjGEMQJoNNDlVHBLAjycQzSYM80dNv0D1Mga7GP9A+MnDJk6t\nHGQC5MqVZQaFtHbVPNGBwY+mj5VVQ6W4xEBFlA9inMPW9dJZCtN9Scb5X1YynOFi\nNqjUYW4zGdSuFpIqv1MulwM/vOEaaVsiSm1AlvXZAoGBAIzwXzybOdG4St2+SHcQ\npi/BBeEiTZyqJmbq6sZSO+TQCf/Q1NRxpqglyHPw8tY2+bEqzOd4g5MFYn0Drw5s\nOVqfLCQQp7mTpjN2+flPXYKIH3azKxpsgmD2mg39kp2SSzJ+AInG52DcLkBtm5mK\nqr7geexPqkCoF84KoP/MElXM\n-----END PRIVATE KEY-----\n"
    data ["client_email"]= "wids-alexa@wids-alexa.iam.gserviceaccount.com"
    data ["client_id"] = "110234009507444192028"
    data ["auth_uri"] = "https://accounts.google.com/o/oauth2/auth"
    data ["token_uri"] = "https://accounts.google.com/o/oauth2/token"
    data ["auth_provider_x509_cert_url"] = "https://www.googleapis.com/oauth2/v1/certs"
    data["client_x509_cert_url"] = "https://www.googleapis.com/robot/v1/metadata/x509/wids-alexa%40wids-alexa.iam.gserviceaccount.com"
    
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(data,scope)
    client = gspread.authorize(creds)
    sheet = client.open("Women Data Scientist Template").sheet1 #insufficient permission
    dataframe = pd.DataFrame(sheet.get_all_records())
    
    return dataframe
    
pattern = re.compile('\((.*?)\)') #remove information between parenthesis
pattern2 = re.compile('\[.*?\]')  #remove all brackets
pattern3 = re.compile('\:\d+') #remove specific footer information

def get_intro_sentence(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')] #wikipedia needs this
    #split text from wiki and not
    urls = url.split('https://en.wikipedia.org/wiki/') 
    resource = opener.open('https://en.wikipedia.org/wiki/' + urllib.parse.quote_plus(urls[1]))
    data = resource.read()
    resource.close()
    soup = BeautifulSoup(data,"lxml")
    sentence = soup.find('div',class_='mw-parser-output')
    #find text in text book and ignore text in there.
    textbox = soup.find_all('table')
    other_text = []
    for t in textbox:
        additional_text = t.find_all('p')
        if len(additional_text)>0:
            for a in additional_text:
                other_text.append(a.text)
    string = []
    #only get introduction text, and break function once we get to 
    #table of contents with an ID of 'toc'
    for s in sentence.descendants:
        if s.name=='p' and s.text not in other_text and s.text !='':
            string.append(s.text)
        elif s.name=='div':
            if 'id' in s.attrs.keys():
                if s.attrs['id']=='toc':
                    break
                    
    #clean text
    string2 = [pattern3.sub("", pattern2.sub("", pattern.sub("", s))) for s in string]
    
    #return text
    if len(string2)==1:
        return string2[0], None
    else:
        return string2[0], string2[1:]
        
def getExpertsFromField(_field,session):
    print("in getExpertsFromField")
    data = pd.read_json(session['attributes']['DataFrame'])
    return data[data['Field'] == _field]

#from random import sample  
def get_expert_in_field(intent, session):
    print("in get_expert_in_field")
    if 'Field' in intent['slots']:
        field = intent['slots']['Field']['value']
        expertData = getExpertsFromField(field,session) 
        expert = expertData.sample(1) 
        
        promptedExperts = session['attributes']['PreviousExperts']
        x=0
        loop = False
        while expert.iloc[0]['Women Name'] in promptedExperts and not loop:
            # This can go into a loop if all experts have been prompted--added loop boolean
            expert = expertData.sample(1)
            x=x+1
            if x>5:
                loop = True
        promptedExperts.append(expert.iloc[0]['Women Name'])
        session['attributes']['PreviousExperts'] = promptedExperts
        session['attributes']['PersonRow'] = expert 
        expertPhrase = get_specific_person(expert.iloc[0]['Women Name'])
        speech_output= expert.iloc[0]['Women Name'] + " is an expert in " + field + expertPhrase
        card_title = expert.iloc[0]['Women Name']
        reprompt_text = ""
        should_end_session = False
        session_attributes = session['attributes']
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))
    else:
        speech_output= "We don't have data on that field."
        card_title = ""
        reprompt_text = ""
        should_end_session = False
        session_attributes = session['attributes']
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))



def get_more_info(session):
    print("in get_more_info")
    session_attributes = session['attributes']
    card_title = "More Information"
    reprompt_text = ""
    should_end_session = False
    
    speech_output = pd.read_json(session_attributes['PersonRow'])['Short Sentence describing what she does'].to_string(index=False) 
        
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
    
    

def get_field(session):
    print("under construction")
    
def get_specific_person(session):
    print("under construction")
    
    

def lambda_handler(event, context):
    if (event["session"]["application"]["applicationId"] != "amzn1.ask.skill.df0a39e0-ed03-4c57-b1b8-a6291d25b2ae"):
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
        return get_inspiration(session)
    elif intent_name == "GetMoreInfoOnFig":
        return get_more_info(session)
    elif intent_name == "GetFieldOfFig":
        return get_field(session)
    elif intent_name == "GetSpecificFig":
        return  get_specific_person(session)
    elif intent_name == "GetExpert":
        return get_expert_in_field(intent,session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response(session) #update need to create
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")
        

def on_session_ended(session_ended_request, session):
    print("Ending session.")
    # Cleanup goes here...

def handle_session_end_request():
    card_title = "BAH - Thank you"
    speech_output = "Thanks for chatting with me. Come back another time."
    should_end_session = True
    
    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))
    
def get_welcome_response():
    print("in get_welcome_response")
    try:
        session_attributes = {'DataFrame': getGoogleSheet().to_json(), 'previousExperts': [], 'PersonRow' : None}
        print("Retrieved google sheet")
    except :
        session_attributes = {'DataFrame':  inspirationDF.to_json(), 'previousExperts': [], 'PersonRow' : None}
    card_title = "BAH"
    speech_output = "Welcome to the Alexa Finding Inspiration Skill. " \
                    "You can ask me who inspires me, or " \
                    "tell me who inspires you."
    reprompt_text = "Please ask me for who inspires me or , " \
                    "ask me about specific inspirational people."
    if pd.read_json(session_attributes['DataFrame']).shape[0]!=0:
        should_end_session = False
    else:
        speech_output = speech_output + \
        "  But we currently have a Google Sheet Error." \
            "Please contact the Booz Allen Team"
        should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_help_response(session):
    print("in get_help_response")
    speech_output = "You can ask me who inspires me, ", \
    "ask me to tell me more about this person, and more"
    reprompt_text = ""
    card_title = "Help"
    should_end_session=False
    session_attributes = session['attributes']
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    
def get_inspiration(session):
    print("in get_inspiration")
    session_attributes = session['attributes']
    card_title = "Inspiration"
    reprompt_text = ""
    should_end_session = False
    
	
    personRow = pd.read_json(session_attributes['DataFrame']).sample(n=1)
    
    #print(personRow)
    #print(type(personRow))
    #print(personRow['Women Name'])
    
    speech_output = personRow['Women Name'].to_string(index=False) + " inspires me."

    session_attributes['PersonRow'] = personRow.to_json()
    
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
