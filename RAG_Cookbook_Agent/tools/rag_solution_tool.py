from crewai.tools import BaseTool
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from crewai import LLM
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class RAGSolutionTool(BaseTool):
    name: str = "RAGSolutionTool"
    description: str = "Check CI/CD logs against cookbook (ChromaDB). If no match, use Gemini LLM to provide a short solution."

    def _run(self, log_input: str) -> str:
        # Step 1: Load embedding model
        embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

        # Step 2: Connect to ChromaDB (new architecture)
        client = chromadb.PersistentClient(path="./chromadb")

        # Step 3: Load existing collection
        try:
            collection = client.get_collection(name="cookbook")
        except Exception as e:
            return f"❌ Error: Could not find 'cookbook' collection. Details: {str(e)}"

        # Step 4: Encode input log
        log_embedding = embedding_model.encode([log_input]).tolist()

        # Step 5: Query the vector DB
        try:
            results = collection.query(
                query_embeddings=log_embedding,
                n_results=1,
                include=["documents", "metadatas", "distances"]
            )
        except Exception as e:
            return f"❌ Error querying ChromaDB: {str(e)}"

        # Step 6: Distance threshold (adjust as needed)
        distance_threshold = 0.35
        match_distance = results["distances"][0][0]
        print(f"🔍 Match Distance: {match_distance}")

        if match_distance < distance_threshold:
            matched_error = results["documents"][0][0]
            solution = results["metadatas"][0][0]["solution"]
            return (
                f" Found in Cookbook\n"
                f" Matched Error: {matched_error}\n"
                f" Solution: {solution}"
            )

        # Step 7: Fallback to Gemini LLM
        llm = LLM(model="gemini/gemini-2.0-flash", provider="google", api_key=GEMINI_API_KEY)
        prompt = f"This log error was not found in the cookbook. Give a short, concise solution for:\n\n'{log_input}'"
        llm_response = llm.call(prompt)

        return f"🤖 Not found in cookbook. Here's a Gemini-generated solution:\n{llm_response}"
