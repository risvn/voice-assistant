## **🧠 RAG (Retrieval-Augmented Generation) with ChromaDB \+ SentenceTransformers**

This project showcases a straightforward, local implementation of **Retrieval-Augmented Generation (RAG)**, leveraging the following:

* 💬 **sentence-transformers**: For generating sophisticated text embeddings.  
* 🗃️ **ChromaDB**: Serving as a persistent, local vector database.  
* 🧾 **Text input**: Sourced directly from .txt files.  
* 🔍 **Semantic search**: To enrich queries with highly relevant contextual information.


**📚 What is RAG?**

**RAG** is an innovative technique that involves **retrieving pertinent information from a custom knowledge base** (such as your own documents or notes) and subsequently **augmenting the prompt** provided to a language model.

This powerful approach empowers the language model to:

* Provide answers deeply **grounded in your proprietary data**.  
* Effectively **circumvent limitations of its context window** and mitigate **hallucination issues**.  
* Operate seamlessly **locally, without requiring an internet connection**.



#### ---------------------------------------------------------------------------------------------------

**📂 Folder Structure**

Bash

rag/  
├── data/               \# 📁 Your input .txt files  
│   └── data.txt  
├── chroma\_db/          \# 📦 Vector DB storage (auto-created)  
├── .filelist.txt       \# 🗂️ Tracks processed files (auto-generated)  
├── rag.py              \# 🧠 Main RAG script  
└── README.md           \# 📘 This file

## **▶️ Usage**

1. **Install dependencies**:  
   Bash  
   pip install sentence-transformers chromadb

2. **Add your .txt files** to the ./data folder.  
3. **Run**:  
   Bash  
   python3 rag.py

   * On the first run, the system will build and store the embeddings.  
   * On subsequent runs, it will intelligently skip reprocessing if the files haven't undergone any changes.

#### ---------------------------------------------------------------------------------------------------

**🔁 Force Rebuilding the DB**

To trigger a complete reindex (e.g., after making edits to your files), simply delete .filelist.txt:

Bash

rm .filelist.txt

Alternatively, just add a new file to the ./data directory.


#### ---------------------------------------------------------------------------------------------------

**🛠️ How It Works**

### **1\. ✂️ Chunking and Embedding**

* Text content from .txt files located in the ./data folder is systematically divided into manageable **chunks** (e.g., approximately 500 words each).  
* Each of these chunks is then transformed into a numerical vector representation using a SentenceTransformer model, such as "all-MiniLM-L6-v2".

### **2\. 🧠 Vector Storage in ChromaDB**

* The generated embeddings are securely stored in a local **ChromaDB** database, which resides in the ./chroma\_db directory.  
* A .filelist.txt file is utilized to diligently track which files have already been indexed, ensuring that the database is updated only when necessary.

### **3\. 🔎 Query & Retrieval**

* When you pose a question, it is first embedded and then intelligently compared against the multitude of stored vectors.  
* The top-matching document chunks are precisely retrieved, forming the crucial **context** for your query.  
* This retrieved context is then seamlessly fed into your Large Language Model (LLM) prompt, typically formatted as:

Use the following context to answer:  
\[retrieved text\]

Question: \[your query\]


**🧪 Example**

Imagine your documents contain detailed information about photosynthesis. If you then ask:

Plaintext

What's photosynthesis?

The script will efficiently locate and return the most relevant chunks from your documents, even if your exact question wasn't explicitly present.
