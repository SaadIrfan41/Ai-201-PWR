import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
print(OPENROUTER_API_KEY)

BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "google/gemini-2.0-flash-exp:free"


def main():
    # Using the OpenRouter API directly
    response = requests.post(
        url=f"{BASE_URL}/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        },
        data=json.dumps(
            {
                "model": MODEL,
                "messages": [{"role": "user", "content": "Tell me a joke?"}],
            }
        ),
    )
    data = response.json()
    print(data["choices"][0]["message"]["content"])


if __name__ == "__main__":
    main()
