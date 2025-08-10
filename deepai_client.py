import os
import requests

DEEPAI_API_KEY = os.getenv("DEEPAI_API_KEY")

def enhance_seo_text(caption):
    if not DEEPAI_API_KEY:
        raise ValueError("DeepAI API key not set in environment variable DEEPAI_API_KEY")

    prompt = f"Create a professional, SEO-optimized title and up to 50 relevant keywords for the image description: {caption}"

    response = requests.post(
        "https://api.deepai.org/api/text-generator",
        data={'text': prompt},
        headers={'api-key': DEEPAI_API_KEY}
    )

    if response.status_code != 200:
        raise RuntimeError(f"DeepAI API error: {response.text}")

    return response.json().get("output", "").strip()
