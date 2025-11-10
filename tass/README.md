# IA de renseignement : groupe 2
### GENTIEU Martin | GUILLAUME 


Ce projet extrait du texte de pages web, puis l'analyse linguistique avec un NER (de Spacy) et un LLM (Mistral).
**L'intégralité du code se fait dans une instance VsCode Python dans Onyxia datalab.**
**La création des index se fera ainsi dans Elastic Search Cloud**

---

## 🚀 Prérequis et Installation

Une fois l'instance VsCode Python ouverte, faites en sorte d'être dans le répertoire nommé **work**.

Suivez ensuite les instructions suivantes.

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/MGentieu/rens.git

2. Installer les paquets nécessaires :
   ```bash
   pip install -r src/requirements.txt
   python -m spacy download en_core_web_trf

L'installation peut prendre 10 minutes.

3. ⚙️ Paramétrez vos variables d'environnement dans le fichier .env, à créer dans le même répertoire que .env.exemple :
   ```env
   MISTRAL_API_KEY="your_api_key"
   ELASTIC_SEARCH_API_KEY="your_api_key"


4. Placez-vous ensuite dans le répertoire src :
   ```bash
   cd tass/src

On pourra ensuite exécuter les scripts python pour bien formater les chemins relatifs entre les dossiers.

5. Il faut également s'assurer de disposer des fichiers JSON suivants qui ne sont pas obtenus à partir du code :
- **100_articles_pour_p3_bis.json**
- **p3_bis_21k_articles**

### **Voici un tableau détaillant les différentes associations des codes / sorties :**

| Phase | Code | Input JSON | Output JSON | Temps d'exécution |
|-----|-----|--------|--------|-------|
| P1 | src/p1.py |---| data/p1_articles.json | quelques secondes |
| P2 | src/p2.py |---| data/p2_articles.json | ~20 minutes |
| P3 | src/p3.py |---| data/p3_articles.json | ~30 à 40 minutes |
| P3 bis | src/p3_bis.py | data/100_articles_sources_pour_p3_bis.json | data/p3_bis_100_articles.json | ~5 minutes |

**Voici également un tableau détaillant les associations pour la 4e phase : la création des index pour Elastic Search Cloud :**

| Description | Code | Input JSON | Output JSON | Index créé |
|-----|-----|--------|--------|---------|
| 100 articles applatis | src/flatten_100_articles.py | data/p3_bis_100_articles.JSON | data/p3_bis_100_articles_flattened.JSON | ---|
| 21k articles applatis | src/flatten_21k_articles.py | data/p3_bis_21k_articles.JSON | data/p3_bis_21k_articles_flattened.JSON | ---|
| Index 100 articles | src/p4_index_cloud_100_articles.py | data/p3_bis_100_articles.JSON |---| press_articles |
| Index 100 articles applatis | src/p4_index_flattened_cloud_100_articles.py | data/p3_bis_100_articles_flattened.JSON |---| press_articles_flattened |
| Index 21k articles | src/p4_index_cloud_21k_articles.py | data/p3_bis_21k_articles.JSON |---| all_press_articles |
| Index 21k articles applatis | src/p4_index_flattened_cloud_21k_articles.py | data/p3_bis_21k_articles_flattened.JSON |---| all_press_articles_flattened |

### Visualisation :

La visualisation des données dans un tableau de bord et l'analyse des résultats est ensuite effectuée dans les fichiers suivants :








