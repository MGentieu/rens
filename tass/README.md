# IA de renseignement : groupe 2

Ce projet extrait du texte de pages web, puis l'analyse linguistique avec **SpaCy**.

---

## 🚀 Installation

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/MGentieu/rens.git

2. Installer les paquets nécessaires :
   ```bash
   pip install -r src/requirements.txt
   python -m spacy download en_core_web_trf

3. Placez-vous ensuite dans le répertoire src :
   ```bash
   cd tass/src

On pourra ensuite exécuter les scripts python pour bien formater les chemins relatifs entre les dossiers.

### **Voici un tableau détaillant les différentes associations des codes / sorties :**

| Phase | Code | Output JSON |
|-----|-----|--------|
| P1 | src/requete_articles_phase1.py | data/articles_phase1.json |
| P2 | src/requete_contenu_phase2.py | data/articles_contenu_phase2.json |
| P3 | src/requete_ner_phase3.py | data/articles_ner_phase3.json |







