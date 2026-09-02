import json
import os
import time
from urllib.request import Request, urlopen

api_key = os.environ["WAVESPEED_API_KEY"]
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
payload = {
    "prompt": "Cinematic aerial shot of a colossal biomechanical city-ship drifting through a nebula at golden hour, intricate organic-metallic architecture covered in bioluminescent veins, massive translucent wings made of light, thousands of tiny ships swarming like fireflies, warm rim lighting against cold cosmic background, shot on 65mm IMAX film, anamorphic lens flares, insane detail, photorealistic, 8K\n\n",
    "num_images": 1
}

def request_json(url, data=None):
    request = Request(url, data=data, headers=headers, method="POST" if data else "GET")
    with urlopen(request) as response:
        return json.load(response)

# 1. Submit the prediction.
submit_body = request_json("https://api.wavespeed.ai/api/v3/x-ai/grok-2-image", json.dumps(payload).encode())
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
