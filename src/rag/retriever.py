
from pathlib import Path
import logging

import chromadb
from sentence_transformers import SentenceTransformer


# ==========================================
# 1. CONFIGURATION
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CHROMA_DIR = PROJECT_ROOT / "data" / "vector_db"

COLLECTION_NAME = "company_knowledge"

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


# ==========================================
# 2. LOGGING
# ==========================================

logger = logging.getLogger(__name__)


# ==========================================
# 3. INITIALIZE COMPONENTS SAFELY
# ==========================================

model = None
client = None
collection = None


def initialize_retriever():

    global model, client, collection

    try:

        logger.info("Loading embedding model...")

        model = SentenceTransformer(
            EMBEDDING_MODEL_NAME
        )

        logger.info("Embedding model loaded.")

        if not CHROMA_DIR.exists():
            raise FileNotFoundError(
                f"ChromaDB directory not found: {CHROMA_DIR}"
            )

        logger.info("Connecting to ChromaDB...")

        client = chromadb.PersistentClient(
            path=str(CHROMA_DIR)
        )

        collection = client.get_collection(
            name=COLLECTION_NAME
        )

        logger.info("ChromaDB connected.")
        logger.info(
            "Stored chunks: %s",
            collection.count()
        )

        return True

    except Exception as error:

        model = None
        client = None
        collection = None

        logger.exception(
            "Retriever initialization failed: %s",
            error
        )

        return False


# Initialize when this module is imported.
initialize_retriever()


# ==========================================
# 4. SEMANTIC SEARCH
# ==========================================

def search_documents(query, top_k=3):

    # Validate query
    if not isinstance(query, str) or not query.strip():
        raise ValueError("Search query cannot be empty.")

    # Validate top_k
    if isinstance(top_k, bool) or not isinstance(top_k, int) or top_k < 1:
        raise ValueError("top_k must be a positive integer.")

    # Check initialization
    if model is None or collection is None:
        raise RuntimeError(
            "Retriever is not initialized. "
            "Check the embedding model and ChromaDB connection."
        )

    try:

        # Generate query embedding
        query_embedding = model.encode(
            query.strip()
        ).tolist()

        # Check database count
        total_chunks = collection.count()

        if total_chunks == 0:
            logger.warning("ChromaDB collection is empty.")
            return []

        # Retrieve relevant chunks
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, total_chunks),
            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )

        documents = results.get("documents") or [[]]
        metadatas = results.get("metadatas") or [[]]
        distances = results.get("distances") or [[]]

        retrieved_documents = []

        for document, metadata, distance in zip(
            documents[0],
            metadatas[0],
            distances[0]
        ):

            retrieved_documents.append({
                "content": document,
                "source": metadata.get("source", "Unknown"),
                "chunk_id": metadata.get("chunk_id", "Unknown"),
                "distance": round(float(distance), 4)
            })

        logger.info(
            "Retrieved %s chunks for query.",
            len(retrieved_documents)
        )

        return retrieved_documents

    except Exception as error:

        logger.exception(
            "Document retrieval failed: %s",
            error
        )

        raise RuntimeError(
            "Unable to retrieve company documents."
        ) from error


# ==========================================
# 5. MANUAL TEST
# ==========================================

if __name__ == "__main__":

    test_questions = [
        "What services does Triads Future offer?",
        "Who are the target customers?",
        "How should sales leads be prioritized?",
        "Who can approve discounts?",
        "How are customer quotations prepared?"
    ]

    if collection is not None:

        for question in test_questions:

            print("\n" + "=" * 65)
            print("QUESTION:", question)
            print("=" * 65)

            try:

                results = search_documents(
                    query=question,
                    top_k=2
                )

                for i, result in enumerate(results, 1):

                    print(f"\nResult {i}")
                    print("Source:", result["source"])
                    print("Chunk ID:", result["chunk_id"])
                    print("Distance:", result["distance"])
                    print("Content:", result["content"])

            except (ValueError, RuntimeError) as error:

                print("SEARCH ERROR:", error)

    else:
        print("Retriever initialization failed.")
