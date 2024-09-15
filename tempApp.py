from flask import Flask
from twilio.rest import Client
from twilio.twiml.voice_response import voice_response
import requests

app = Flask(__name__)

BASETEN_API_KEY = "YMKFudUr.FcjOTi13DlaR3ZtCbBIumoXeqFJy25yx" 
BASETEN_MODEL_ID = "8w6yyp2q"
TWILIO_PHONE_NUMBER = "+18557295038"

account_sid = "AC9f06f684fe4f7db4930e1ac021123561"
auth_token = "b40ce8a6260d575947ce58e4693316f1"
client = Client(account_sid, auth_token)

@app.route('/start_call', methods=['POST'])
def start_call():
    data = request.json
    to_number = data.get('to_number')
    initial_message = data.get('message')

    call = twilio_client.calls.create(
        url=f"http://127.0.0.1:5000/handle_call?message={initial_message}",
        to= to_number, 
        from_ = TWILIO_PHONE_NUMBER
    )

    return jsonify({"message": "call started", "call_sid": call.sid})

@app.route('/handle_call', methods=['POST'])
def handle_call():
    response = VoiceResponse()
    message = request.args.get('message') or requests.form.get('SpeechResult')

    if message:
        llm_response = generate_llm_response(message)
        response.say(llm_response)
    response.gather(input)

    return str(response)

def generate_llm_response(user_input):
    url = f"https://model-{BASETEN_MODEL_ID}.api.basetn.co/production/predict"
    headers={"Authorization": f"Api-Key {BASETEN_API_KEY}"},
    payload = {
        "prompt": f"In a phone conversation with spiderman, respond to: {user_input}"
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()['output']
    else:
        return "I'm sorry, I'm having trouble understanding. Can you please repeat that?"

if __name__ == '__main__':
    app.run(debug=True)




'''
call = client.calls.create(
    url="http://demo.twilio.com/docs/voice.xml",
    to="+15109800215",
    from_="+18557295038",
)
'''