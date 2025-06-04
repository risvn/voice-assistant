from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# opening the documents :
def open_files(file_path):
    # write logic for handling different files pdf,docs,html,txt
    with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()


#basic text-processing for now
def clean_data(text):
     text = text.strip().replace('\r\n', '\n').replace('\t', ' ')
    return text



def split_into_chunks(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
        chunk = chunk.lower()
    return chunks


# 1. Load the model
model = SentenceTransformer("all-MiniLM-L6-v2")


# 3. Encode to get embeddings
embeddings = model.encode(chunks)



































