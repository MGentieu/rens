import os
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv("../.env.exemple")
api_key = os.getenv("MISTRAL_API_KEY")
model = "mistral-large-latest"

client = Mistral(api_key=api_key)
messages = [
    {
        "role": "user",
        "content": "What is the best French meal? Return the name and the ingredients in short JSON object.",
    }
]
chat_response = client.chat.complete(
      model = model,
      messages = messages,
      response_format = {
          "type": "json_object",
      }
)