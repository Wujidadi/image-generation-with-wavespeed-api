const apiKey = process.env.WAVESPEED_API_KEY;
if (!apiKey) throw new Error("Set WAVESPEED_API_KEY");

const headers = { Authorization: `Bearer ${apiKey}`, "Content-Type": "application/json" };
async function requestJson(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) throw new Error(await response.text());
  return response.json();
}

// 1. Submit the prediction.
const submitBody = await requestJson("https://api.wavespeed.ai/api/v3/x-ai/grok-imagine-image-v2.0/edit", {
  method: "POST",
  headers,
  body: JSON.stringify({
  "images": [
    "https://static.wavespeed.ai/examples/a9611516b3bb4352b23df9cbbd1dd7b6/1786699724406346329_ZfoyHPZ9-094bff173b1f.webp"
  ],
  "prompt": "Transform her into a stylish pirate captain while preserving her face and overall stance. Replace the outfit with a dark navy pirate coat, leather belt, tall boots, and layered accessories. Add a dramatic pirate ship behind her, wind-blown sails, treasure chest details, and a bold adventurous atmosphere. Keep the image realistic, cinematic, and detailed.",
  "resolution": "2k",
  "quality": "medium"
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
