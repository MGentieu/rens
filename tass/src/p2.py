import json
import requests
from bs4 import BeautifulSoup
import time

# Charger les articles depuis le fichier JSON
with open("../data/p1_articles.json", "r", encoding="utf-8") as f:
    data = json.load(f)

base_url = "https://tass.com"
articles = data.get("newsList", [])

# Liste pour stocker les articles enrichis
enriched_articles = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

i = 1
for article in articles:
    url = base_url + article["link"]
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Extraire le texte principal
            content_div = soup.find("div", class_="text-content")
            paragraphs = content_div.find_all("p") if content_div else []
            full_text = "\n".join(p.get_text(strip=True) for p in paragraphs)

            # Extraire les tags
            tags_div = soup.find("div", class_="tags")
            tags = [a.get_text(strip=True) for a in tags_div.find_all("a")] if tags_div else []

            # Ajouter au dictionnaire
            article["text"] = full_text
            article["tags"] = tags
            enriched_articles.append(article)

            print(f"✅ Article {i} : id = {article['id']} récupéré")
        else:
            print(f"❌ Article {i} : id = {article['id']} erreur HTTP {response.status_code}")
        i = i+1
    except Exception as e:
        print(f"⚠️ {article['id']} erreur : {e}")

    time.sleep(0.3)  # Pause pour éviter de surcharger le serveur

# Sauvegarder les articles enrichis
with open("../data/p2_articles.json", "w", encoding="utf-8") as f:
    json.dump({"newsList": enriched_articles}, f, ensure_ascii=False, indent=2)

print("✅ Tous les articles enrichis ont été sauvegardés dans p2_articles.json")
