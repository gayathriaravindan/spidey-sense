from flask import Flask, request, jsonify
from flask_cors import CORS
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
import logging
import requests

app = Flask(__name__)
CORS(app)

BASETEN_API_KEY = "YMKFudUr.FcjOTi13DlaR3ZtCbBIumoXeqFJy25yx" 
MODEL_ID = "8w6yyp2q"
TWILIO_PHONE_NUMBER = "+18557295038"

account_sid = "AC9f06f684fe4f7db4930e1ac021123561"
auth_token = "89b25e97bfb8c45c40ee630abd2f8964"
client = Client(account_sid, auth_token)

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def main():
    return "hello, world"

@app.route('/start_call', methods=['GET', 'POST'])
def start_call():
    try:
        # Replace with your TwiML Bin URL
        twiml_bin_url = 'https://handler.twilio.com/twiml/EH332f6a8867e846cbfa4422c507e6c1fc'

        # Initiate the call with the TwiML Bin URL
        call = client.calls.create(
            url=twiml_bin_url,  # Use the TwiML Bin URL here
            to="+15109800215",   # The phone number to call
            from_=TWILIO_PHONE_NUMBER
        )
        
        logging.info(f"Call initiated with SID: {call.sid}")
        return jsonify({"message": "Call started", "call_sid": call.sid})
    
    except Exception as e:
        logging.error(f"Error in start_call: {str(e)}")
        return jsonify({"error": str(e)}), 500
    


@app.route('/handle_response', methods=['POST'])
def handle_response():
    # Get the user's speech input
    user_input = request.form.get('SpeechResult', '')

    # Log the input
    logging.debug(f"Received speech input: {user_input}")

    # Generate LLM response
    llm_response = generate_llm_response(user_input)
    logging.info(f"LLM response: {llm_response}")

    # Create a new TwiML response
    response = VoiceResponse()
    response.say(llm_response)
    response.gather(input='speech', action='/handle_response', method='POST')

    return str(response)




def generate_llm_response(user_input):
    messages = [
        {"role": "system", "content": "You are spiderman who is getting a call to save someone. Ask questions or generate a reply like \"On my way in 15\""},
        {"role": "user", "content": user_input},
    ]

    payload = {
    "messages": messages,
    "stream": True,
    "max_tokens": 2048,
    "temperature": 0.9
    }
    res = requests.post(
        f"https://model-{MODEL_ID}.api.baseten.co/production/predict",
        headers={"Authorization": f"Api-Key {BASETEN_API_KEY}"},
        json=payload,
        stream=True
    )
    return (res.text)
    

if __name__ == '__main__':
    # Make sure the app runs locally on port 5000
    app.run(host='127.0.0.1', port=5000)
