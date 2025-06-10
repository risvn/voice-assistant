import sys
from pathlib import Path
import os
# Include ../bin/core in the import path
sys.path.append(str(Path(__file__).resolve().parent.parent / "core"))
from core.wiki import get_summary
#from core.nearby import find_nearby
from core.headlines import fetch_top_headlines
from core.weather import get_detailed_weather


from rag import get_rag_prompt



# --- Query classification ---
KEYWORDS = {

    "weather": ["cool","temperature","weather"],
    "rag": ["rag","docs","documents","text","find","search"],
    "nearby": ["near me", "nearby", "closest", "around me", "in my area"],
    "headlines": ["news", "headlines", "breaking news", "latest news"],
    "wiki": ["who","who is",  "when did", "wikip", "tell me about"],
}

def classify_query(query: str) -> str:
    query_lower = query.lower()
    for category, keywords in KEYWORDS.items():
        if any(keyword in query_lower for keyword in keywords):
            return category
    return "default"

# --- Prompt generator ---
def generate_prompt(context: str, query: str, system_prompt: str = "You are a helpful assistant.") -> str:
    return f"""<|system|>
{system_prompt}
<|user|>
Use the following context to answer the question:
If the answer is not present in the context, respond with "I don't know."
--------------------
{context}
--------------------

Question: {query}
<|assistant|>"""

# --- Main dispatcher ---
def get_context_and_prompt(query: str) -> str:
    category = classify_query(query)

    if category == "weather":
        context = get_detailed_weather("hyderabad")
        return generate_prompt(context, query)
    elif category == "nearby":
        # Uncomment once you define `find_nearby`
        # context = find_nearby(query)
        context = "Nearby search is not implemented yet."
        return generate_prompt(context, query)
    elif category == "rag":
        context = get_rag_prompt(query)
        return generate_prompt(context, query)
    elif category == "wiki":
        context = get_summary(query)
        return generate_prompt(context, query)
    elif category == "headlines":
        context = fetch_top_headlines()
        return generate_prompt(context, query)
    else:
        # Just return the query in a plain prompt

          return f"""<|system|>
You are a thoughtful and emotionally intelligent assistant. 
You respond briefly, insightfully, and always stay open to feedback. 
After answering, you wait for feedback from the user, and if they give any, you improve your response accordingly.
<|user|>
{query}
<|assistant|>"""





# --- CLI entrypoint ---
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("query", type=str, help="User query")
    args = parser.parse_args()

    print(get_context_and_prompt(args.query))

