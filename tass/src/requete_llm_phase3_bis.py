import os
from mistralai import Mistral
from dotenv import load_dotenv
import json

load_dotenv("../.env.exemple")
api_key = os.getenv("MISTRAL_API_KEY")
model = "mistral-medium-2508"
client = Mistral(api_key=api_key)

prompt = """You are an assistant responsible for analyzing news articles.
For each article, you must add a structured field containing a semantic analysis.
Here are the expected fields:
"""

structured_output = '''
"structured": {
    "topics": [
        "military exercises",
        "anti-terrorism"
    ],
    "overall_sentiment": 0.0,
    "sentiment_by_country": [
        {
            "country": "TJ",
            "sentiment": 0.0
        },
        {
            "country": "RU",
            "sentiment": 0.0
        },
        {
            "country": "AM",
            "sentiment": 0.0
        },
        {
            "country": "BY",
            "sentiment": 0.0
        },
        {
            "country": "KZ",
            "sentiment": 0.0
        },
        {
            "country": "KG",
            "sentiment": 0.0
        },
        {
            "country": "UZ",
            "sentiment": 0.0
        }
    ],
    "actors_mentioned": [
        "Commonwealth of Independent States (CIS)",
        "Collective Security Treaty Organization (CSTO)",
        "Armenia",
        "Belarus",
        "Kazakhstan",
        "Kyrgyzstan",
        "Russia",
        "Tajikistan",
        "Uzbekistan"
    ],
    "article_type": "report",
    "id": 2034673
}

'''


"""
strctured
topics: the 2 main themes of the article, expressed in English (e.g., "military", "technology", "politics", "economy", "diplomacy", "environment", "health", "science", etc.).


overall_sentiment: a global sentiment score between -1 (very negative) and 1 (very positive), with neutral sentiment close to 0.


sentiment_by_country: a list of objects { "country": "<ISO alpha-2 code>", "sentiment": <float> } corresponding to the countries mentioned in the article.


If a country is mentioned positively, the score should be close to 1; if negatively, close to -1.




actor_mentioned: a list of actors or organizations mentioned that play a role in the article.


article_type: choose exactly one type from the following list:
["report", "analysis", "opinion", "interview", "investigation", "breaking_news", "feature"]

"""

# Charger les articles depuis le fichier JSON
with open("../data/source_json_pour_llm.json", "r", encoding="utf-8") as f:
    data = json.load(f)

articles = data.get("newsList", [])

# Liste pour stocker les articles enrichis
enriched_articles = []
for article in articles:
    try:
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
        #enriched_articles.append(article)
    except Exception as e:
        print(f"⚠️ {article['id']} erreur : {e}")

# Sauvegarder les articles enrichis
with open("../data/articles_remplis_phase3_bis.json", "w", encoding="utf-8") as f:
    json.dump({"newsList": enriched_articles}, f, ensure_ascii=False, indent=2)

print("✅ Tous les articles enrichis ont été sauvegardés dans articles_enrichis.json")

