# Setup

import requests
MODEL_ID = "8w6yyp2q"
BASETEN_API_KEY = "YMKFudUr.FcjOTi13DlaR3ZtCbBIumoXeqFJy25yx" # Paste from Discord

# Basic inference with streaming output

# The notebook may cut off streaming output, calling the model from the terminal instead could help.

messages = [
    {"role": "system", "content": "You are an expert software developer serving as a mentor at the HackMIT hackathon."},
    {"role": "user", "content": "What are some hackathon project ideas?"},
]

payload = {
    "messages": messages,
    "stream": True,
    "max_tokens": 2048,
    "temperature": 0.9
}

# Call model endpoint
res = requests.post(
    f"https://model-{MODEL_ID}.api.baseten.co/production/predict",
    headers={"Authorization": f"Api-Key {BASETEN_API_KEY}"},
    json=payload,
    stream=True
)

# Print the generated tokens as they get streamed
for content in res.iter_content():
    print(content.decode("utf-8"), end="", flush=True)

# Basic inference without streaming

# Again, the notebook may cut off the full output.

messages = [
    {"role": "system", "content": "You are an expert software developer serving as a mentor at the HackMIT hackathon."},
    {"role": "user", "content": "What are some hackathon project ideas?"},
]

payload = {
    "messages": messages,
    "stream": False,
    "max_tokens": 2048,
    "temperature": 0.9
}

# Call model endpoint
res = requests.post(
    f"https://model-{MODEL_ID}.api.baseten.co/production/predict",
    headers={"Authorization": f"Api-Key {BASETEN_API_KEY}"},
    json=payload,
    stream=False
)

# Print the generated tokens as they get streamed
print(res.text)
     