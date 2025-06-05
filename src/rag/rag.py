from sentence_transformers import SentenceTransformer
import chromadb
import re
import os


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



def update_db(data_dir="./data", db_dir="./chroma_db", filelist_path="./data/filelist.txt"):
    """Rebuild DB only if new or different filenames are found in ./data."""
    current_files = sorted(os.listdir(data_dir))
    
    if os.path.exists(filelist_path):
        with open(filelist_path, 'r') as f:
            saved_files = f.read().splitlines()

        if current_files == saved_files:
            return False
        else:
            print("data fiels have been changed,removing old db")

    with open(filelist_path, 'w') as f:
        f.write("\n".join(current_files))

    # Clear old DB
    if os.path.exists(db_dir):
        import shutil
        shutil.rmtree(db_dir)
        print(" Old DB removed.")

    return True
update_db()

def store_embeddings(chunks, embeddings):
    """Store chunks and embeddings to ChromaDB."""
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection("my_documents")

    if len(collection.peek()["ids"]) == 0:
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


def query_embeddings(collection, model, query, n_results=2):
    """Query ChromaDB for relevant documents."""
    query_embedding = model.encode([query])[0].tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    return results['documents']


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
    retrieved_docs = query_embeddings(collection, model, query)

    print("🔍 Retrieved:", retrieved_docs)
