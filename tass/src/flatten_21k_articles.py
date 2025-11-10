import json

articles = []
with open("../data/p3_bis_21k_articles.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

flattened_articles = []

i = 0
for article in articles:
    id = article.get("id")
    print(f"Article {i} : id = {id}")

    structured = sentiment_list = article.get("structured", {})
    if structured is None: # On vérifie que l'attribut structured existe bien. Sinon, on ignore l'article et on passe au suivant.
        continue

    sentiment_list = structured.get("sentiment_by_country", [])
    if not sentiment_list:
        continue

    for s in sentiment_list:
        flattened_articles.append({
            "id": article.get("id"),
            "mark": article.get("mark"),
            "date": article.get("date"),
            "title": article.get("title"),
            "country": s.get("country"),
            "sentiment": s.get("sentiment")
        })
        
    print(f"Article {i} : id = {id} fini")
    i = i+1

# --- Écriture du résultat dans un fichier JSON ---
output_file = "../data/p3_bis_21k_articles_flattened.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(flattened_articles, f, indent=2, ensure_ascii=False)

print(f"✅ {i} articles traités et enregistrés dans {output_file}")