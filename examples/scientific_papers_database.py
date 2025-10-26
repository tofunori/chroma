"""
Base de données pour articles scientifiques avec Chroma
========================================================

Ce script montre comment créer une base de données pour stocker et rechercher
des articles scientifiques en utilisant Chroma.
"""

import chromadb
from typing import List, Dict


def create_scientific_papers_db():
    """
    Crée une base de données pour articles scientifiques avec Chroma.
    """

    # Créer un client Chroma persistant (les données sont sauvegardées sur disque)
    client = chromadb.PersistentClient(path="./scientific_papers_db")

    # Créer ou récupérer une collection pour les articles
    collection = client.get_or_create_collection(
        name="scientific_papers",
        metadata={"description": "Collection d'articles scientifiques"}
    )

    return client, collection


def add_paper(collection, paper_id: str, title: str, abstract: str,
              authors: List[str], year: int, journal: str = None,
              keywords: List[str] = None, doi: str = None):
    """
    Ajoute un article scientifique à la collection.

    Args:
        collection: La collection Chroma
        paper_id: Identifiant unique de l'article
        title: Titre de l'article
        abstract: Résumé de l'article
        authors: Liste des auteurs
        year: Année de publication
        journal: Nom du journal (optionnel)
        keywords: Mots-clés (optionnel)
        doi: DOI de l'article (optionnel)
    """

    # Combiner titre et abstract pour une meilleure recherche
    document_text = f"Titre: {title}\n\nRésumé: {abstract}"

    # Créer les métadonnées
    metadata = {
        "title": title,
        "authors": ", ".join(authors),
        "year": year,
    }

    if journal:
        metadata["journal"] = journal
    if keywords:
        metadata["keywords"] = ", ".join(keywords)
    if doi:
        metadata["doi"] = doi

    # Ajouter à la collection
    collection.add(
        documents=[document_text],
        metadatas=[metadata],
        ids=[paper_id]
    )

    print(f"✓ Article ajouté: {title}")


def search_papers(collection, query: str, n_results: int = 5,
                  year_min: int = None, year_max: int = None):
    """
    Recherche des articles scientifiques par requête en langage naturel.

    Args:
        collection: La collection Chroma
        query: Requête de recherche en langage naturel
        n_results: Nombre de résultats à retourner
        year_min: Année minimale (optionnel)
        year_max: Année maximale (optionnel)

    Returns:
        Résultats de la recherche
    """

    # Construire le filtre de métadonnées si nécessaire
    where_filter = None
    if year_min is not None or year_max is not None:
        where_filter = {}
        if year_min is not None:
            where_filter["year"] = {"$gte": year_min}
        if year_max is not None:
            if "year" in where_filter:
                where_filter["year"]["$lte"] = year_max
            else:
                where_filter["year"] = {"$lte": year_max}

    # Effectuer la recherche
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where=where_filter,
        include=["documents", "metadatas", "distances"]
    )

    return results


def display_results(results):
    """
    Affiche les résultats de recherche de manière lisible.
    """
    if not results["ids"][0]:
        print("Aucun résultat trouvé.")
        return

    print(f"\n{'='*80}")
    print(f"Trouvé {len(results['ids'][0])} résultat(s):")
    print(f"{'='*80}\n")

    for i, (doc, metadata, distance) in enumerate(zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ), 1):
        print(f"{i}. {metadata['title']}")
        print(f"   Auteurs: {metadata['authors']}")
        print(f"   Année: {metadata['year']}")
        if 'journal' in metadata:
            print(f"   Journal: {metadata['journal']}")
        if 'keywords' in metadata:
            print(f"   Mots-clés: {metadata['keywords']}")
        if 'doi' in metadata:
            print(f"   DOI: {metadata['doi']}")
        print(f"   Score de similarité: {1 - distance:.3f}")
        print()


def main():
    """
    Exemple d'utilisation de la base de données d'articles scientifiques.
    """

    print("=== Base de données d'articles scientifiques avec Chroma ===\n")

    # Créer la base de données
    client, collection = create_scientific_papers_db()

    # Ajouter quelques exemples d'articles
    print("\n1. Ajout d'articles à la base de données...\n")

    add_paper(
        collection,
        paper_id="paper_001",
        title="Deep Learning for Medical Image Analysis",
        abstract="This paper presents a comprehensive survey of deep learning methods "
                 "applied to medical image analysis. We discuss convolutional neural networks, "
                 "transfer learning, and their applications in disease detection and diagnosis.",
        authors=["Smith, J.", "Johnson, A.", "Williams, B."],
        year=2023,
        journal="Medical Imaging Review",
        keywords=["deep learning", "medical imaging", "CNN", "diagnosis"],
        doi="10.1234/mir.2023.001"
    )

    add_paper(
        collection,
        paper_id="paper_002",
        title="Climate Change and Biodiversity Loss in Tropical Forests",
        abstract="We investigate the impact of climate change on biodiversity in tropical "
                 "rainforests. Our study shows a significant correlation between rising "
                 "temperatures and species extinction rates over the past 50 years.",
        authors=["Garcia, M.", "Chen, L.", "Patel, R."],
        year=2022,
        journal="Nature Climate Science",
        keywords=["climate change", "biodiversity", "tropical forests", "extinction"],
        doi="10.1234/ncs.2022.045"
    )

    add_paper(
        collection,
        paper_id="paper_003",
        title="Quantum Computing Algorithms for Cryptography",
        abstract="This work explores novel quantum algorithms for breaking classical "
                 "cryptographic systems and proposes new quantum-resistant encryption methods. "
                 "We demonstrate the potential threats and solutions in the quantum era.",
        authors=["Zhang, W.", "Kumar, S."],
        year=2024,
        journal="Quantum Information Processing",
        keywords=["quantum computing", "cryptography", "algorithms", "security"],
        doi="10.1234/qip.2024.012"
    )

    add_paper(
        collection,
        paper_id="paper_004",
        title="Machine Learning for Drug Discovery",
        abstract="We present a machine learning framework for predicting drug-target "
                 "interactions and accelerating the drug discovery process. Our model "
                 "achieves 92% accuracy on benchmark datasets.",
        authors=["Brown, E.", "Davis, K.", "Wilson, T."],
        year=2023,
        journal="Computational Biology Journal",
        keywords=["machine learning", "drug discovery", "bioinformatics"],
        doi="10.1234/cbj.2023.078"
    )

    # Effectuer des recherches
    print("\n2. Exemples de recherches...\n")

    # Recherche 1: Intelligence artificielle en médecine
    print("RECHERCHE 1: Articles sur l'IA en médecine")
    results = search_papers(
        collection,
        query="artificial intelligence and machine learning in medical applications",
        n_results=3
    )
    display_results(results)

    # Recherche 2: Changement climatique
    print("\nRECHERCHE 2: Articles sur le changement climatique")
    results = search_papers(
        collection,
        query="environmental impact and climate change",
        n_results=3
    )
    display_results(results)

    # Recherche 3: Articles récents (2023 et après)
    print("\nRECHERCHE 3: Articles récents sur l'informatique quantique (2023+)")
    results = search_papers(
        collection,
        query="quantum computing",
        n_results=3,
        year_min=2023
    )
    display_results(results)

    # Statistiques de la collection
    print(f"\n{'='*80}")
    print(f"Total d'articles dans la base de données: {collection.count()}")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
