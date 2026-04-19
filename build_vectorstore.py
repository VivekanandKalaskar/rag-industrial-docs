# build_vectorstore.py
# Combine everything: load PDFs → chunk → embed → store in ChromaDB

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import chromadb
import os

# --- Step 1: Load PDFs ---
docs_folder = "C:\D\Rag\documents"
all_documents = []

for filename in os.listdir(docs_folder):
    if filename.endswith(".pdf"):
        filepath = os.path.join(docs_folder, filename)
        print(f"Loading: {filename}")
        loader = PyPDFLoader(filepath)
        all_documents.extend(loader.load())

print(f"\nTotal pages loaded: {len(all_documents)}")

# --- Step 2: Chunk ---
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " "]
)
chunks = splitter.split_documents(all_documents)
chunks = [c for c in chunks if len(c.page_content.strip()) >= 150]
print(f"Meaningful chunks: {len(chunks)}")

# --- Step 3: Embed and store ---
print("\nLoading embedding model...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

print("Building vector store (this may take a minute)...")

# Create a persistent ChromaDB client explicitly
client = chromadb.PersistentClient(path="chroma_db")

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    client=client,
    collection_name="industrial_docs"
)

print(f"\nDone! Vector store saved with {vectorstore._collection.count()} vectors")
print("Saved to: chroma_db/")

# --- Step 4: Quick test search ---
print("\n--- Test Search ---")
query = "How to prevent electrical hazards?"
results = vectorstore.similarity_search_with_score(query, k=3)

for i, (doc, score) in enumerate(results):
    print(f"\nResult {i+1} (score: {score:.4f}):")
    print(f"  Source: {doc.metadata['source']}")
    print(f"  Page: {doc.metadata['page']}")
    print(f"  Content: {doc.page_content[:200]}...")