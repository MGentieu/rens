import json
import spacy
from collections import defaultdict

# Charger le modèle spaCy
nlp = spacy.load("en_core_web_trf")

# Fichier d'entrée / sortie
INPUT_FILE = "../data/p2_articles.json"
OUTPUT_FILE = "../data/p3_articles.json"

# Labels ciblés
target_labels = {"PERSON", "ORG", "GPE", "PRODUCT", "EVENT"}

def keep_longest_if_substring(entities):
    # 1) Dédoublonnage insensible à la casse en gardant la version la plus longue
    mapping = {}  # lower -> best original
    for e in entities:
        key = e.lower()
        if key in mapping:
            # garde la version la plus longue (ou la première si même longueur)
            if len(e) > len(mapping[key]):
                mapping[key] = e
        else:
            mapping[key] = e

    unique = list(mapping.values())
    lowered = [u.lower() for u in unique]

    # 2) Supprimer les éléments qui sont strictement contenus dans un autre
    keep = []
    for i, e in enumerate(unique):
        e_low = lowered[i]
        is_sub = False
        for j, other_low in enumerate(lowered):
            if i == j:
                continue
            if e_low in other_low and len(other_low) > len(e_low):
                is_sub = True
                break
        if not is_sub:
            keep.append(e)

    return sorted(keep)

# Charger les articles depuis le fichier JSON
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Traitement des articles
i = 1
for article in data.get("newsList", []):
    text = article.get("text", "")
    if not text or not text.strip():
        article["ner"] = {}
        continue

    doc = nlp(text)

    # Dictionnaire trié par label
    ner_by_label = defaultdict(set)
    for ent in doc.ents:
        if ent.label_ in target_labels:
            ner_by_label[ent.label_].add(ent.text)

    # Pour chaque label, garder uniquement la/les chaînes les plus longues en cas de sous-chaînes
    cleaned = {}
    for label, entities in ner_by_label.items():
        cleaned[label] = keep_longest_if_substring(sorted(entities))

    article["ner"] = cleaned
    print(f"Article {i} fini")
    i = i+1

# Sauvegarder dans un nouveau fichier
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ Extraction NER terminée. Résultat dans {OUTPUT_FILE}")
