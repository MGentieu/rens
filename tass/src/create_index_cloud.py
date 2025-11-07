import json
from elasticsearch import Elasticsearch, helpers
from dotenv import load_dotenv
import os


cloud_url = "https://a687f6d1571f4f6ab6f8c80b66f8af15.us-central1.gcp.cloud.es.io:443"  # ← ton URL cloud
index_name = "press_articles"
load_dotenv("../.env")
api_key = os.getenv("ELASTIC_SEARCH_API_KEY")

# --- Connexion Elasticsearch Cloud ---
es = Elasticsearch(
    cloud_url,
    api_key=api_key,
    verify_certs=True  # en production, toujours True
)

# --- Vérifier la connexion ---
if es.ping():
    print("✅ Connexion réussie à Elasticsearch Cloud")
else:
    print("❌ Échec de la connexion au cluster")

if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, mappings={
       "properties": {
            "id": {"type": "long"},
            "isFlash": {"type": "integer"},
            "isOnline": {"type": "integer"},
            "type": {"type": "keyword"},
            "mark": {"type": "text"},
            "date": {"type": "date", "format": "epoch_second"},
            "title": {"type": "text"},
            "subtitle": {"type": "text"},
            "lead": {"type": "text"},
            "image": {"type": "keyword"},
            "link": {"type": "keyword"},
            "sponsor_id": {"type": "long", "null_value": -1},
            "sponsor_type_id": {"type": "long", "null_value": -1},
            "text": {"type": "text"},
            "tags": {"type": "keyword"},
            "ner": {
                "properties": {
                    "PERSON": {"type": "keyword"},
                    "ORG": {"type": "keyword"},
                    "GPE": {"type": "keyword"},
                    "PRODUCT": {"type": "keyword"}
                }
            },
            "semantic_analysis": {
                "properties": {
                    "topics": {"type": "keyword"},
                    "overall_sentiment": {"type": "float"},
                    "sentiment_by_country": {
                        "type": "nested",
                        "properties": {
                            "country": {"type": "keyword"},
                            "sentiment": {"type": "float"}
                        }
                    },
                    "actor_mentioned": {"type": "keyword"},
                    "article_type": {"type": "keyword"}
                }
            }
        }
    }
)
    print(f"Index '{index_name}' created.")
else:
    print(f"Index '{index_name}' already exists.")

# 🔹 Charger le fichier JSON
with open("../data/articles_structured_phase3bis.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

# 🔹 Préparer les documents pour bulk insert
actions = []
for article in articles:
    actions.append({
        "_index": index_name,
        "_id": article["id"],  # optionnel : utiliser l'id existant comme _id
        "_source": article
    })

# 🔹 Insérer tous les documents en bulk
helpers.bulk(es, actions)
print(f"{len(actions)} articles indexed successfully into '{index_name}'.")
