 # load_documents.py
# Step 1 of RAG: Load PDF documents and extract text

from langchain_community.document_loaders import PyPDFLoader
import os

# Point to your documents folder
docs_folder = "C:\D\Rag\documents"

# Load every PDF in the folder
all_documents = []

for filename in os.listdir(docs_folder):
    if filename.endswith(".pdf"):
        filepath = os.path.join(docs_folder, filename)
        print(f"Loading: {filename}")
        
        # PyPDFLoader reads the PDF and splits it into pages
        loader = PyPDFLoader(filepath)
        pages = loader.load()
        
        all_documents.extend(pages)
        print(f"  → {len(pages)} pages loaded")

print(f"\nTotal: {len(all_documents)} pages from {len(os.listdir(docs_folder))} files")

# Let's peek at what a "document" looks like
print("\n--- Sample Page ---")
print(f"Source: {all_documents[0].metadata['source']}")
print(f"Page: {all_documents[0].metadata['page']}")
print(f"Content preview: {all_documents[0].page_content[:300]}...")