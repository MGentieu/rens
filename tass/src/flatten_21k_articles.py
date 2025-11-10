import json

articles = []
with open("../data/articles_structured_phase3bis.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

flattened_articles = []

for article in articles:
    sentiment_list = article.get("semantic_analysis", {}).get("sentiment_by_country", [])
    for s in sentiment_list:
        flattened_articles.append({
            "id": article.get("id"),
            "mark": article.get("mark"),
            "date": article.get("date"),
            "title": article.get("title"),
            "country": s.get("country"),
            "sentiment": s.get("sentiment")
        })

# --- Écriture du résultat dans un fichier JSON ---
output_file = "../data/flattened_structured_articles.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(flattened_articles, f, indent=2, ensure_ascii=False)

print(f"✅ {len(flattened_articles)} articles traités et enregistrés dans {output_file}")