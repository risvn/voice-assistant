import sys
from pathlib import Path

# Include ../core and ../rag in the import path
base = Path(__file__).resolve().parent.parent
sys.path.append(str(base / "core"))
sys.path.append(str(base / "rag"))

from core.wiki import get_summary
from core.headlines import fetch_top_headlines
from core.weather import get_detailed_weather

from rag import (
    split_into_chunks,
    store_embeddings,
    query_embeddings,
    generate_prompt as rag_generate_prompt,
)
from sentence_transformers import SentenceTransformer

# --- Query classification ---
KEYWORDS = {
    "weather": ["cool","temperature","weather"],
    "nearby": ["near me", "nearby", "closest", "around me", "in my area"],
    "headlines": ["news", "headlines", "breaking news", "latest news"],
    "wiki": ["who","who is", "when did", "wikip", "tell me about"],
    "rag": ["rag", "document search", "knowledge base", "local data"]
}

# --- System Prompt ---
DEFAULT_SYSTEM_PROMPT = "You are a helpful assistant."

# --- Classify query ---
def classify_query(query: str) -> str:
    query_lower = query.lower()
    for category, keywords in KEYWORDS.items():
        if any(keyword in query_lower for keyword in keywords):
            return category
    return "default"

# --- Main dispatcher ---
def get_context_and_prompt(query: str) -> str:
    category = classify_query(query)

    if category == "weather":
        context = get_detailed_weather("hyderabad")
        return rag_generate_prompt(context, query, DEFAULT_SYSTEM_PROMPT)

    elif category == "nearby":
        context = "Nearby search is not implemented yet."
        return rag_generate_prompt(context, query, DEFAULT_SYSTEM_PROMPT)

    elif category == "wiki":
        context = get_summary(query)
        return rag_generate_prompt(context, query, DEFAULT_SYSTEM_PROMPT)

    elif category == "headlines":
        context = fetch_top_headlines()
        return rag_generate_prompt(context, query, DEFAULT_SYSTEM_PROMPT)

    elif category == "rag":
        try:
            print("📚 Using RAG for knowledge base search...")
            with open(base / "rag/data/data.txt") as f:
                text = f.read()

            model = SentenceTransformer("all-MiniLM-L6-v2")
            chunks = split_into_chunks(text)
            embeddings = model.encode(chunks).tolist()

            collection = store_embeddings(chunks, embeddings)
            results = query_embeddings(collection, model, query)
            context = "\n".join([r for r in results[0]])

            return rag_generate_prompt(context, query, DEFAULT_SYSTEM_PROMPT)

        except Exception as e:
            print("❌ RAG error:", e)
            return f"""<|system|>
{DEFAULT_SYSTEM_PROMPT}
<|user|>
{query}
<|assistant|>"""

    else:
        # 🧠 DEFAULT fallback to plain conversation prompt
        return f"""<|system|>
You are a thoughtful and emotionally intelligent chat companion.
You respond in a short, insightful, and engaging manner—like a friend.
Use natural, language ask feed back on your response.

<|user|>
{query}
<|assistant|>"""

# --- Allow command-line testing ---
if __name__ == "__main__":
    query = sys.argv[1]
    print(get_context_and_prompt(query))
