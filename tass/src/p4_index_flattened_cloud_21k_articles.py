import json
from elasticsearch import Elasticsearch, helpers
from dotenv import load_dotenv
import os


cloud_url = "https://a687f6d1571f4f6ab6f8c80b66f8af15.us-central1.gcp.cloud.es.io:443"  # ← ton URL cloud
index_name = "all_press_articles_flattened"
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

# 🔹 Créer l'index (si il n'existe pas)
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, mappings={
       "properties": {
            "id": {"type": "long"},
            "mark": {"type": "text"},
            "date": {"type": "date", "format": "epoch_second"},
            "title": {"type": "text"},
            "country": {"type": "keyword"},
            "sentiment": {"type": "float"}
        }
    }
)
    print(f"Index '{index_name}' created.")
else:
    print(f"Index '{index_name}' already exists.")

# 🔹 Charger le fichier JSON
with open("../data/p3_bis_21k_articles_flattened.json", "r", encoding="utf-8") as f:
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
