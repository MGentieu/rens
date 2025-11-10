import json
from elasticsearch import Elasticsearch, helpers

# 🔹 Connexion à Elasticsearch
# Assumes Elasticsearch is at localhost:9200 and using the password from your .env
es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "elastic"),
    verify_certs=False  # changez avec votre ELASTIC_PASSWORD
)

# 🔹 Nom de l'index
index_name = "index1"

# 🔹 Créer l'index (si il n'existe pas)
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
with open("../data/p3_bis_100_articles.json", "r", encoding="utf-8") as f:
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

