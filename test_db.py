# test_db.py
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import chromadb

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="chroma_db")

vectorstore = Chroma(
    client=client,
    collection_name="industrial_docs",
    embedding_function=embeddings
)

count = vectorstore._collection.count()
print(f"Vectors in store: {count}")

if count > 0:
    results = vectorstore.similarity_search("electrical hazards", k=2)
    for i, doc in enumerate(results):
        print(f"\nResult {i+1}: {doc.page_content[:200]}")
else:
    print("Vector store is empty!")