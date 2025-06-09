
from sentence_transformers import SentenceTransformer
import chromadb
import re
import os

#pre-processing the text and making in to the chunks
def split_into_chunks(text, max_words=50, overlap=10):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    chunks = []
    current_chunk = []

    for sentence in sentences:
        words = sentence.split()
        if len(current_chunk) + len(words) <= max_words:
            current_chunk.extend(words)
        else:
            if current_chunk:
                chunks.append(' '.join(current_chunk).lower())
                current_chunk = words[-overlap:]  # overlap from the previous
            else:
                chunks.append(' '.join(words).lower())

    if current_chunk:
        chunks.append(' '.join(current_chunk).lower())

    return chunks


#if any files are changed in ./data the chroma_db is created 
def store_embeddings(chunks, embeddings, data_dir="./data", db_dir="./chroma_db", filelist_path="./data/.filelist.txt"):
    """Check if data has changed. Rebuild Chroma DB if so. Always return a valid collection."""
    current_files = sorted(os.listdir(data_dir))

    data_changed = True
    if os.path.exists(filelist_path):
        with open(filelist_path, 'r') as f:
            saved_files = f.read().splitlines()
        if current_files == saved_files:
            data_changed = False
        else:
            print("🔁 Data files have changed. Rebuilding DB...")
    else:
        print("📂 No filelist found. Assuming first run.")

    # Save new filelist
    with open(filelist_path, 'w') as f:
        f.write("\n".join(current_files))

    # Remove old DB if needed
    if data_changed and os.path.exists(db_dir):
        import shutil
        shutil.rmtree(db_dir)
        print("🧹 Old DB removed.")

    # Create or reuse DB
    client = chromadb.PersistentClient(path=db_dir)
    collection = client.get_or_create_collection("my_documents")

    if data_changed or len(collection.peek()["ids"]) == 0:
        print("✅ Adding new documents...")
        collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=[f"doc{i}" for i in range(len(chunks))]
        )
        print("✅ Documents added.")
    else:
        print("✅ Already indexed. Skipping.")

    return collection


#seraching the qurey-embeddings from the chroma_db
def query_embeddings(collection, model, query, n_results=2):
    """Query ChromaDB for relevant documents."""
    query_embedding = model.encode([query])[0].tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    return results['documents']

#generates the prompt_templet after getting context from rag-pipeline
def generate_prompt(context: str, query: str, system_prompt: str = "You are a helpful assistant.") -> str:
    prompt = f"""<|system|>
{system_prompt}
<|user|>
Use the following context to answer the question:
If the answer is not present in the context, respond with "I don't know."
--------------------
{context}
--------------------

Question: {query}
<|assistant|>
"""
    return prompt



# --- Public wrapper to call full RAG prompt ---
def get_rag_prompt(query: str) -> str:
    """Run full RAG pipeline and return generated prompt for a query."""
    data_path = "./data/data.txt"
    model = SentenceTransformer("all-MiniLM-L6-v2")

    with open(data_path) as f:
        text = f.read()

    chunks = split_into_chunks(text)
    embeddings = model.encode(chunks).tolist()

    collection = store_embeddings(chunks, embeddings)
    results = query_embeddings(collection, model, query)

    return results


if __name__ == "__main__":
    # Load text
    with open("./data/data.txt") as f:
        text = f.read()

    # Init model
    print("🔄 Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Preprocess & embed
    print("📄 Splitting and embedding text...")
    chunks = split_into_chunks(text)
    embeddings = model.encode(chunks).tolist()

    # Store
    collection = store_embeddings(chunks, embeddings)

    # Query
    query = "what is social media"
    context = query_embeddings(collection, model, query)
    
    #prompt
    prompt=generate_prompt(context,query)
    print(prompt)
