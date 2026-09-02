import json
import os
import time
from urllib.request import Request, urlopen

api_key = os.environ["WAVESPEED_API_KEY"]
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
payload = {
    "prompt": "A charismatic foreign man in his early thirties standing outside a luxurious desert casino at dusk, wearing an emerald-green tailored suit, open-collar shirt, polished black shoes, and a gold signet ring, holding poker chips and a playing card, vintage cars and glowing signage behind him, desert wind lifting dust across the ground, stylish cinematic vibe, rich details, realistic editorial photography.",
    "aspect_ratio": "1:1",
    "resolution": "2k",
    "quality": "medium"
}

def request_json(url, data=None):
    request = Request(url, data=data, headers=headers, method="POST" if data else "GET")
    with urlopen(request) as response:
        return json.load(response)

# 1. Submit the prediction.
submit_body = request_json("https://api.wavespeed.ai/api/v3/x-ai/grok-imagine-image-v2.0/text-to-image", json.dumps(payload).encode())
task = submit_body.get("data", submit_body)
prediction_id = task.get("id")
if not prediction_id:
    raise RuntimeError("Submission response did not contain a prediction id")
result_url = f"https://api.wavespeed.ai/api/v3/predictions/{prediction_id}/result"

# 2. Poll until the prediction finishes.
while True:
    body = request_json(result_url)
    result = body.get("data", body)
    status = result.get("status")
    if status == "completed":
        print(result.get("outputs", []))
        break
    if status in {"failed", "cancelled", "timeout", "deleted"}:
        raise RuntimeError(result)
    time.sleep(2)
