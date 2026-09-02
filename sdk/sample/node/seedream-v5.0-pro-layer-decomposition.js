const apiKey = process.env.WAVESPEED_API_KEY;
if (!apiKey) throw new Error("Set WAVESPEED_API_KEY");

const headers = { Authorization: `Bearer ${apiKey}`, "Content-Type": "application/json" };
async function requestJson(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) throw new Error(await response.text());
  return response.json();
}

// 1. Submit the prediction.
const submitBody = await requestJson("https://api.wavespeed.ai/api/v3/bytedance/seedream-v5.0-pro/layer-decomposition", {
  method: "POST",
  headers,
  body: JSON.stringify({
  "image": "https://static.wavespeed.ai/examples/14fce2c809424e518b3ea5b26bbc62c6/1786523194712036881_qT3clvEN-45bfc3ba100a.webp",
  "resolution": "1k",
  "output_format": "png",
  "prompt_optimization_mode": "standard"
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
