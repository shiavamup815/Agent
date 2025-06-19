import json
import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

def create_chroma_store(json_path="RAG_Cookbook_Agent/cookbook.json", persist_dir="./chromadb"):
    # Load cookbook
    with open(json_path, "r") as f:
        cookbook = json.load(f)["log_cookbook"]

    # Load embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")
    documents = [entry["error_message"] for entry in cookbook]
    embeddings = model.encode(documents).tolist()

    # ✅ NEW CLIENT INITIALIZATION (no legacy config)
    client = chromadb.PersistentClient(path=persist_dir)

    # Delete old collection if it exists
    try:
        client.delete_collection("cookbook")
    except:
        pass

    # Create new collection
    collection = client.create_collection(name="cookbook")

    collection.add(
        documents=documents,
        embeddings=embeddings,
        ids=[str(i) for i in range(len(documents))],
        metadatas=[{"solution": entry["solution"]} for entry in cookbook]
    )

    print("✅ ChromaDB vector store created and persisted.")

if __name__ == "__main__":
    create_chroma_store()
