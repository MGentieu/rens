import json


def flatten_semantic(article):
    """Aplati l'attribut semantic_analysis d'un article"""
    semantic = article.pop("semantic_analysis", {})
    for key, value in semantic.items():
        article[f"semantic_analysis_{key}"] = value
    return article

articles = []
with open("../data/articles_structured_phase3bis.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

# --- Traitement de la liste complète ---
flattened_articles = [flatten_semantic(article.copy()) for article in articles]

# --- Écriture du résultat dans un fichier JSON ---
output_file = "../data/flattened_structured_articles.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(flattened_articles, f, indent=2, ensure_ascii=False)

print(f"✅ {len(flattened_articles)} articles traités et enregistrés dans {output_file}")