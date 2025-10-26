# Base de données d'articles scientifiques avec Chroma

Ce guide vous montre comment créer et utiliser une base de données pour rechercher vos articles scientifiques avec Chroma.

## 🚀 Démonstration rapide

Essayez la démo interactive qui montre toutes les fonctionnalités :

```bash
# Installer Chroma
pip install chromadb

# Lancer la démonstration
python scientific_papers_demo_with_embeddings.py
```

Cette démo crée une base avec 6 articles scientifiques et effectue plusieurs recherches pour montrer :
- Ajout d'articles avec métadonnées
- Recherche sémantique en langage naturel
- Filtrage par année
- Affichage de tous les articles

## Installation

```bash
pip install chromadb
```

## Utilisation rapide

### 1. Exécuter l'exemple complet

```bash
python scientific_papers_database.py
```

### 2. Exécuter la démo simple

```bash
python scientific_papers_demo_with_embeddings.py
```

### 3. Code minimal pour commencer

```python
import chromadb

# Créer un client persistant
client = chromadb.PersistentClient(path="./mes_articles")

# Créer une collection
collection = client.get_or_create_collection(name="scientific_papers")

# Ajouter un article
collection.add(
    documents=["Titre: Mon article\n\nRésumé: Ceci est mon résumé..."],
    metadatas=[{
        "title": "Mon article",
        "authors": "Dupont, J., Martin, A.",
        "year": 2024,
        "journal": "Nature"
    }],
    ids=["article_001"]
)

# Rechercher
results = collection.query(
    query_texts=["machine learning"],
    n_results=5
)

# Afficher les résultats
for metadata in results["metadatas"][0]:
    print(f"{metadata['title']} ({metadata['year']})")
```

## Fonctionnalités principales

### Ajouter des articles

```python
collection.add(
    documents=["Titre + résumé de l'article"],
    metadatas=[{
        "title": "Titre",
        "authors": "Auteur1, Auteur2",
        "year": 2024,
        "journal": "Nom du journal",
        "keywords": "mot-clé1, mot-clé2",
        "doi": "10.1234/example"
    }],
    ids=["unique_id"]
)
```

### Rechercher par similarité sémantique

```python
# Recherche en langage naturel
results = collection.query(
    query_texts=["articles sur le machine learning en médecine"],
    n_results=10
)
```

### Filtrer par métadonnées

```python
# Rechercher uniquement les articles récents
results = collection.query(
    query_texts=["deep learning"],
    n_results=5,
    where={"year": {"$gte": 2023}}  # Année >= 2023
)

# Rechercher par auteur
results = collection.query(
    query_texts=["neural networks"],
    where={"authors": {"$contains": "Smith"}}
)
```

### Recherche combinée

```python
# Recherche avec filtres multiples
results = collection.query(
    query_texts=["climate change"],
    n_results=10,
    where={
        "$and": [
            {"year": {"$gte": 2020}},
            {"journal": "Nature"}
        ]
    }
)
```

## Cas d'usage avancés

### 1. Importer des articles depuis un fichier PDF

```python
# Vous pouvez utiliser PyPDF2 ou pdfplumber pour extraire le texte
import PyPDF2

def extract_pdf_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

# Ajouter à Chroma
text = extract_pdf_text("mon_article.pdf")
collection.add(
    documents=[text],
    metadatas=[{"title": "Mon article", "year": 2024}],
    ids=["article_pdf_001"]
)
```

### 2. Importer depuis BibTeX

```python
import bibtexparser

# Lire un fichier BibTeX
with open('references.bib') as bib_file:
    bib_database = bibtexparser.load(bib_file)

# Ajouter chaque entrée à Chroma
for entry in bib_database.entries:
    collection.add(
        documents=[entry.get('abstract', '')],
        metadatas=[{
            "title": entry.get('title', ''),
            "authors": entry.get('author', ''),
            "year": int(entry.get('year', 0)),
            "journal": entry.get('journal', ''),
        }],
        ids=[entry['ID']]
    )
```

### 3. Intégration avec des APIs (ArXiv, PubMed, etc.)

```python
import arxiv

# Rechercher sur ArXiv
search = arxiv.Search(
    query="machine learning",
    max_results=10
)

# Ajouter à Chroma
for result in search.results():
    collection.add(
        documents=[f"Title: {result.title}\n\nAbstract: {result.summary}"],
        metadatas=[{
            "title": result.title,
            "authors": ", ".join([a.name for a in result.authors]),
            "year": result.published.year,
            "arxiv_id": result.entry_id
        }],
        ids=[result.entry_id]
    )
```

## Avantages pour la recherche scientifique

1. **Recherche sémantique** : Trouvez des articles par sens, pas seulement par mots-clés
2. **Pas besoin de configuration complexe** : Simple à mettre en place
3. **Recherche multilingue** : Fonctionne avec différentes langues
4. **Évolutif** : Des centaines de milliers d'articles
5. **Métadonnées riches** : Filtrez par année, auteur, journal, etc.
6. **Persistance** : Vos données sont sauvegardées automatiquement

## Exemples de requêtes

```python
# Trouver des articles similaires à un concept
collection.query(query_texts=["transfer learning in computer vision"])

# Trouver des méthodologies
collection.query(query_texts=["methods for statistical analysis"])

# Trouver des applications spécifiques
collection.query(query_texts=["applications of AI in healthcare"])

# Recherche par domaine
collection.query(
    query_texts=["quantum physics"],
    where={"year": {"$gte": 2020}}
)
```

## Mise à jour et suppression

```python
# Mettre à jour un article
collection.update(
    ids=["article_001"],
    documents=["Nouveau texte"],
    metadatas=[{"title": "Nouveau titre", "year": 2024}]
)

# Supprimer un article
collection.delete(ids=["article_001"])

# Supprimer par filtre
collection.delete(where={"year": {"$lt": 2010}})
```

## Mode client-serveur (pour équipes)

Si vous voulez partager la base de données avec votre équipe :

```bash
# Démarrer le serveur
chroma run --path /chemin/vers/db --host 0.0.0.0 --port 8000

# Se connecter depuis Python
client = chromadb.HttpClient(host="adresse.serveur", port=8000)
```

## Ressources

- Documentation Chroma : https://docs.trychroma.com
- Chroma Cloud (hébergé) : https://trychroma.com
- Exemples : https://github.com/chroma-core/chroma/tree/main/examples

## Support

Pour toute question :
- Discord Chroma : https://discord.gg/MMeYNTmh3x
- Documentation : https://docs.trychroma.com
