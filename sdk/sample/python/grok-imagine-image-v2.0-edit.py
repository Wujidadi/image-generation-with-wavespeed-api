import json
import os
import time
from urllib.request import Request, urlopen

api_key = os.environ["WAVESPEED_API_KEY"]
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
payload = {
    "images": [
        "https://static.wavespeed.ai/examples/a9611516b3bb4352b23df9cbbd1dd7b6/1786699724406346329_ZfoyHPZ9-094bff173b1f.webp"
    ],
    "prompt": "Transform her into a stylish pirate captain while preserving her face and overall stance. Replace the outfit with a dark navy pirate coat, leather belt, tall boots, and layered accessories. Add a dramatic pirate ship behind her, wind-blown sails, treasure chest details, and a bold adventurous atmosphere. Keep the image realistic, cinematic, and detailed.",
    "resolution": "2k",
    "quality": "medium"
}

def request_json(url, data=None):
    request = Request(url, data=data, headers=headers, method="POST" if data else "GET")
    with urlopen(request) as response:
        return json.load(response)

# 1. Submit the prediction.
submit_body = request_json("https://api.wavespeed.ai/api/v3/x-ai/grok-imagine-image-v2.0/edit", json.dumps(payload).encode())
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
