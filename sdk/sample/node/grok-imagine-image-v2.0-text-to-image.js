const apiKey = process.env.WAVESPEED_API_KEY;
if (!apiKey) throw new Error("Set WAVESPEED_API_KEY");

const headers = { Authorization: `Bearer ${apiKey}`, "Content-Type": "application/json" };
async function requestJson(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) throw new Error(await response.text());
  return response.json();
}

// 1. Submit the prediction.
const submitBody = await requestJson("https://api.wavespeed.ai/api/v3/x-ai/grok-imagine-image-v2.0/text-to-image", {
  method: "POST",
  headers,
  body: JSON.stringify({
  "prompt": "A charismatic foreign man in his early thirties standing outside a luxurious desert casino at dusk, wearing an emerald-green tailored suit, open-collar shirt, polished black shoes, and a gold signet ring, holding poker chips and a playing card, vintage cars and glowing signage behind him, desert wind lifting dust across the ground, stylish cinematic vibe, rich details, realistic editorial photography.",
  "aspect_ratio": "1:1",
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
