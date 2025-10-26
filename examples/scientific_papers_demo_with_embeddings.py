"""
Démonstration de base de données pour articles scientifiques avec Chroma
=========================================================================

Cette version fournit ses propres embeddings pour contourner les problèmes de téléchargement.
Dans un cas réel, vous utiliseriez l'embedding automatique de Chroma.
"""

import chromadb
import random


def simple_hash_embedding(text: str, dimensions: int = 384) -> list:
    """
    Crée un embedding simple basé sur le hachage du texte.
    ATTENTION: Ceci est juste pour la démo ! En production, utilisez les vrais embeddings de Chroma.
    """
    random.seed(hash(text.lower()) % (10 ** 8))
    return [random.random() for _ in range(dimensions)]


def main():
    """
    Démonstration de l'utilisation de Chroma pour articles scientifiques.
    """

    print("=" * 80)
    print("BASE DE DONNÉES D'ARTICLES SCIENTIFIQUES AVEC CHROMA")
    print("=" * 80)
    print()
    print("Note: Cette démo utilise des embeddings simplifiés pour la démonstration.")
    print("En production, Chroma génère automatiquement des embeddings sémantiques.")
    print()

    # Créer un client Chroma en mémoire
    print("✓ Création du client Chroma...")
    client = chromadb.Client()

    # Créer une collection
    collection = client.create_collection(
        name="scientific_papers",
        metadata={"description": "Collection d'articles scientifiques"}
    )
    print("✓ Collection 'scientific_papers' créée")
    print()

    # Articles scientifiques
    papers = [
        {
            "id": "paper_001",
            "title": "Deep Learning for Medical Image Analysis",
            "abstract": "This paper presents a comprehensive survey of deep learning methods "
                       "applied to medical image analysis. We discuss convolutional neural networks, "
                       "transfer learning, and their applications in disease detection and diagnosis. "
                       "Our review covers recent advances in CNN architectures for medical imaging.",
            "authors": "Smith, J., Johnson, A., Williams, B.",
            "year": 2023,
            "journal": "Medical Imaging Review",
            "keywords": "deep learning, medical imaging, CNN, diagnosis, AI healthcare"
        },
        {
            "id": "paper_002",
            "title": "Climate Change and Biodiversity Loss in Tropical Forests",
            "abstract": "We investigate the impact of climate change on biodiversity in tropical "
                       "rainforests. Our study shows a significant correlation between rising "
                       "temperatures and species extinction rates over the past 50 years. "
                       "We analyze ecosystem disruption and environmental degradation patterns.",
            "authors": "Garcia, M., Chen, L., Patel, R.",
            "year": 2022,
            "journal": "Nature Climate Science",
            "keywords": "climate change, biodiversity, tropical forests, extinction, environment"
        },
        {
            "id": "paper_003",
            "title": "Quantum Computing Algorithms for Cryptography",
            "abstract": "This work explores novel quantum algorithms for breaking classical "
                       "cryptographic systems and proposes new quantum-resistant encryption methods. "
                       "We demonstrate the potential threats and solutions in the quantum era. "
                       "Focus on post-quantum cryptography and quantum security protocols.",
            "authors": "Zhang, W., Kumar, S.",
            "year": 2024,
            "journal": "Quantum Information Processing",
            "keywords": "quantum computing, cryptography, algorithms, security, encryption"
        },
        {
            "id": "paper_004",
            "title": "Machine Learning for Drug Discovery and Development",
            "abstract": "We present a machine learning framework for predicting drug-target "
                       "interactions and accelerating the drug discovery process. Our model "
                       "achieves 92% accuracy on benchmark datasets. Applications include "
                       "pharmaceutical research and computational biology for medicine.",
            "authors": "Brown, E., Davis, K., Wilson, T.",
            "year": 2023,
            "journal": "Computational Biology Journal",
            "keywords": "machine learning, drug discovery, bioinformatics, AI healthcare, pharma"
        },
        {
            "id": "paper_005",
            "title": "Neural Networks for Natural Language Processing",
            "abstract": "This paper explores transformer architectures and attention mechanisms "
                       "for various NLP tasks including translation, sentiment analysis, and "
                       "question answering. We achieve state-of-the-art results on multiple benchmarks. "
                       "Deep learning applications in language understanding and generation.",
            "authors": "Lee, S., Martinez, R.",
            "year": 2024,
            "journal": "ACL Proceedings",
            "keywords": "NLP, transformers, attention, neural networks, deep learning, AI"
        },
        {
            "id": "paper_006",
            "title": "Renewable Energy Systems and Smart Grid Technology",
            "abstract": "Analysis of renewable energy integration in modern smart grids. "
                       "We present optimization algorithms for energy distribution and storage. "
                       "Focus on solar and wind power systems with AI-based management.",
            "authors": "Anderson, P., Thompson, M.",
            "year": 2023,
            "journal": "Energy Systems Review",
            "keywords": "renewable energy, smart grid, solar power, wind energy, optimization"
        }
    ]

    # Ajouter les articles avec des embeddings personnalisés
    print("Ajout des articles à la base de données...")
    print("-" * 80)

    for paper in papers:
        # Créer le texte du document
        document_text = f"Title: {paper['title']}\n\nAbstract: {paper['abstract']}\n\nKeywords: {paper['keywords']}"

        # Générer un embedding basé sur le contenu
        embedding = simple_hash_embedding(document_text)

        # Ajouter à la collection
        collection.add(
            documents=[document_text],
            embeddings=[embedding],
            metadatas=[{
                "title": paper["title"],
                "authors": paper["authors"],
                "year": paper["year"],
                "journal": paper["journal"],
                "keywords": paper["keywords"]
            }],
            ids=[paper["id"]]
        )
        print(f"  ✓ {paper['title']}")

    print()
    print(f"✓ Total: {collection.count()} articles dans la base de données")
    print()

    # Effectuer des recherches
    print("=" * 80)
    print("EXEMPLES DE RECHERCHES SÉMANTIQUES")
    print("=" * 80)
    print()

    searches = [
        ("Intelligence artificielle pour la santé",
         "AI healthcare deep learning medical diagnosis treatment applications machine learning"),

        ("Changement climatique et environnement",
         "climate change environmental impact biodiversity ecosystem global warming"),

        ("Sécurité informatique quantique",
         "quantum computing cryptography security encryption algorithms protection"),

        ("Énergies renouvelables",
         "renewable energy solar wind power sustainable green technology"),
    ]

    for search_label, search_query in searches:
        print(f"🔍 RECHERCHE: '{search_label}'")
        print("-" * 80)

        # Créer un embedding pour la requête
        query_embedding = simple_hash_embedding(search_query)

        # Rechercher
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3,
            include=["documents", "metadatas", "distances"]
        )

        display_results(results)
        print()

    # Recherche avec filtre par année
    print("🔍 RECHERCHE AVEC FILTRE: Articles de 2024 uniquement")
    print("-" * 80)
    query_embedding = simple_hash_embedding("latest research new findings recent studies")
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5,
        where={"year": {"$eq": 2024}},
        include=["documents", "metadatas", "distances"]
    )
    display_results(results)
    print()

    # Obtenir tous les articles
    print("=" * 80)
    print("TOUS LES ARTICLES DANS LA BASE")
    print("=" * 80)
    all_papers = collection.get(include=["metadatas"])
    for i, metadata in enumerate(all_papers["metadatas"], 1):
        print(f"{i}. {metadata['title']} ({metadata['year']})")
        print(f"   {metadata['authors']}")

    print()
    print("=" * 80)
    print("STATISTIQUES")
    print("=" * 80)
    print(f"📊 Total d'articles: {collection.count()}")
    print(f"📅 Années: 2022-2024")
    print(f"🏷️  Domaines: IA, Médecine, Climat, Quantum, Énergie")
    print()
    print("✅ Démonstration terminée avec succès!")
    print()
    print("💡 Pour utiliser cette base de données dans votre propre projet:")
    print("   1. Installez Chroma: pip install chromadb")
    print("   2. Laissez Chroma gérer les embeddings automatiquement")
    print("   3. Ajoutez vos propres articles scientifiques")
    print("   4. Recherchez en langage naturel!")
    print()


def display_results(results):
    """
    Affiche les résultats de manière lisible.
    """
    if not results["ids"][0]:
        print("  ❌ Aucun résultat trouvé.")
        return

    for i, (metadata, distance) in enumerate(zip(
        results["metadatas"][0],
        results["distances"][0]
    ), 1):
        similarity = max(0, 1 - distance)
        print(f"\n  {i}. 📄 {metadata['title']}")
        print(f"     👥 Auteurs: {metadata['authors']}")
        print(f"     📅 Année: {metadata['year']}")
        print(f"     📚 Journal: {metadata['journal']}")
        print(f"     🏷️  Mots-clés: {metadata['keywords']}")
        print(f"     ⭐ Score: {similarity:.1%}")


if __name__ == "__main__":
    main()
