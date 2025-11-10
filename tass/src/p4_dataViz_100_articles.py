from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

load_dotenv("../.env")
api_key = os.getenv("ELASTIC_SEARCH_API_KEY")
model = "mistral-medium-2508"

client = Elasticsearch(
    "https://a687f6d1571f4f6ab6f8c80b66f8af15.us-central1.gcp.cloud.es.io:443",
    api_key=api_key
)
index_name = "press_articles"
mappings = {
    "properties": {
        "id": {"type": "long"},
        "isFlash": {"type": "int"}
    }
}
mapping_response = client.indices.put_mapping(index=index_name, body=mappings)
print(mapping_response)