# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
#account_sid = os.getenv("TWILIO_ACCOUNT_SID")
#auth_token = os.getenv("TWILIO_AUTH_TOKEN")
account_sid = "AC9f06f684fe4f7db4930e1ac021123561"
auth_token = "b40ce8a6260d575947ce58e4693316f1"
client = Client(account_sid, auth_token)

call = client.calls.create(
    url="http://demo.twilio.com/docs/voice.xml",
    to="+15109800215",
    from_="+18557295038",
)

print(call.sid)