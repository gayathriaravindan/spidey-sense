from flask import Flask, request, jsonify
from flask_cors import CORS
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
import logging
import requests

app = Flask(__name__)
CORS(app)

BASETEN_API_KEY = "YMKFudUr.FcjOTi13DlaR3ZtCbBIumoXeqFJy25yx" 
BASETEN_MODEL_ID = "8w6yyp2q"
TWILIO_PHONE_NUMBER = "+18557295038"

account_sid = "AC9f06f684fe4f7db4930e1ac021123561"
auth_token = "b40ce8a6260d575947ce58e4693316f1"
client = Client(account_sid, auth_token)

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def main():
    return "hello, world"

@app.route('/start_call', methods=['GET', 'POST'])
def start_call():
    # Create a TwiML response
    logging.info("start_call function called")
    try:
        # Create a TwiML response
        response = VoiceResponse()
        
        # Add the initial message
        response.say("Hi, I'm Twilio calling to inform you about Rishita, who is currently in danger at Georgia Tech Avenue.")
        
        # Add a gather for speech input, redirect to your ngrok URL in the action
        response.gather(input='speech', action='https://cd91-192-54-222-158.ngrok-free.app/handle_response', method='POST')
        
        # Initiate the call with the TwiML
        call = client.calls.create(
            twiml=str(response),
            to="+15109800215",  # Your verified Twilio number
            from_=TWILIO_PHONE_NUMBER
        )
        
        logging.info(f"Call initiated with SID: {call.sid}")
        return jsonify({"message": "Call started", "call_sid": call.sid})
    except Exception as e:
        logging.error(f"Error in start_call: {str(e)}")
        return jsonify({"error": str(e)}), 500



@app.route('/handle_response', methods=['POST'])
def handle_response():
    # Log all incoming data for debugging
    logging.info("handle_response function called")
    logging.debug(f"Received POST data: {request.form}")

    # Get the user's speech input
    user_input = request.form.get('SpeechResult', '')

    # Create a new TwiML response
    response = VoiceResponse()

    if not user_input:
        logging.warning("No speech input received")
        response.say("I'm sorry, I didn't catch that. Could you please repeat?")
        response.gather(input='speech', action='https://cd91-192-54-222-158.ngrok-free.app/handle_response', method='POST')
        return str(response)

    logging.info(f"Transcribed speech: {user_input}")
    response.say("Got it, thanks")

    

    '''
    # Generate LLM response based on the user's input
    llm_response = generate_llm_response(user_input)
    logging.info(f"LLM response: {llm_response}")

    # Respond with the LLM response
    response.say(llm_response)

    # Add another gather for continued conversation
    response.gather(input='speech', action='https://c300-192-54-222-158.ngrok-free.app/handle_response', method='POST')

    return str(response)

    '''

def generate_llm_response(user_input):
    url = f"https://model-{BASETEN_MODEL_ID}.api.baseten.co/production/predict"
    headers = {"Authorization": f"Api-Key {BASETEN_API_KEY}"}
    payload = {
        "prompt": f"In a phone conversation with spiderman, respond to: {user_input}"
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['output']
        else:
            return "I'm sorry, I'm having trouble understanding. Can you please repeat that?"
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    # Make sure the app runs locally on port 5000
    app.run(host='127.0.0.1', port=5000)


'''
from flask import Flask, request, jsonify
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
import logging
import requests

app = Flask(__name__)

BASETEN_API_KEY = "YMKFudUr.FcjOTi13DlaR3ZtCbBIumoXeqFJy25yx" 
BASETEN_MODEL_ID = "8w6yyp2q"
TWILIO_PHONE_NUMBER = "+18557295038"

account_sid = "AC9f06f684fe4f7db4930e1ac021123561"
auth_token = "b40ce8a6260d575947ce58e4693316f1"
client = Client(account_sid, auth_token)

@app.route('/')
def main():
    return "hello, world"

@app.route('/start_call', methods=['GET', 'POST'])
def start_call():
    # Create a TwiML response
    response = VoiceResponse()
    
    # Add the initial message
    response.say("Hi, I'm Twilio calling to inform you about Rishita, who is currently in danger at Georgia Tech Avenue.")
    
    # Add a gather for speech input
    response.gather(input='speech', action='/handle_response', method='POST')

    # Initiate the call with the TwiML
    call = client.calls.create(
        twiml=str(response),
        to="+15109800215",
        from_=TWILIO_PHONE_NUMBER
    )

    return jsonify({"message": "Call started", "call_sid": call.sid})

logging.basicConfig(level=logging.DEBUG)

@app.route('/handle_response', methods=['GET','POST'])
def handle_response():
    # Log all incoming data
    logging.debug(f"Received POST data: {request.form}")

    # Get the user's speech input
    user_input = request.form.get('SpeechResult', '')
    
    if not user_input:
        logging.warning("No speech input received")
        response = VoiceResponse()
        response.say("I'm sorry, I didn't catch that. Could you please repeat?")
        response.gather(input='speech', action='/handle_response', method='POST')
        return str(response)

    logging.info(f"Transcribed speech: {user_input}")

    # Generate LLM response
    llm_response = generate_llm_response(user_input)
    logging.info(f"LLM response: {llm_response}")

    # Create a new TwiML response
    response = VoiceResponse()
    response.say(llm_response)

    # Add another gather for continued conversation
    response.gather(input='speech', action='/handle_response', method='POST')

    return str(response)
    
    # Generate LLM response
    llm_response = generate_llm_response(user_input)

    # Create a new TwiML response
    response = VoiceResponse()
    response.say(llm_response)

    # Add another gather for continued conversation
    response.gather(input='speech', action='/handle_response', method='POST')

    return str(response)
   

def generate_llm_response(user_input):
    url = f"https://model-{BASETEN_MODEL_ID}.api.baseten.co/production/predict"
    headers = {"Authorization": f"Api-Key {BASETEN_API_KEY}"}
    payload = {
        "prompt": f"In a phone conversation with spiderman, respond to: {user_input}"
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['output']
        else:
            return "I'm sorry, I'm having trouble understanding. Can you please repeat that?"
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(host='127.0.0.1') '''