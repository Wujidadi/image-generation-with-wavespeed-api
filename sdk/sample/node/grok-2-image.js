const apiKey = process.env.WAVESPEED_API_KEY;
if (!apiKey) throw new Error("Set WAVESPEED_API_KEY");

const headers = { Authorization: `Bearer ${apiKey}`, "Content-Type": "application/json" };
async function requestJson(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) throw new Error(await response.text());
  return response.json();
}

// 1. Submit the prediction.
const submitBody = await requestJson("https://api.wavespeed.ai/api/v3/x-ai/grok-2-image", {
  method: "POST",
  headers,
  body: JSON.stringify({
  "prompt": "Cinematic aerial shot of a colossal biomechanical city-ship drifting through a nebula at golden hour, intricate organic-metallic architecture covered in bioluminescent veins, massive translucent wings made of light, thousands of tiny ships swarming like fireflies, warm rim lighting against cold cosmic background, shot on 65mm IMAX film, anamorphic lens flares, insane detail, photorealistic, 8K\n\n",
  "num_images": 1
}),
});
const task = submitBody.data ?? submitBody;
const predictionId = task.id;
if (!predictionId) throw new Error("Submission response did not contain a prediction id");
const resultUrl = `https://api.wavespeed.ai/api/v3/predictions/${predictionId}/result`;

// 2. Poll until the prediction finishes.
while (true) {
  const body = await requestJson(resultUrl, {
    headers: { Authorization: `Bearer ${apiKey}` },
  });
  const result = body.data ?? body;
  if (result.status === "completed") {
    console.log(result.outputs);
    break;
  }
  if (["failed", "cancelled", "timeout", "deleted"].includes(result.status)) throw new Error(JSON.stringify(result));
  await new Promise(resolve => setTimeout(resolve, 2000));
}
