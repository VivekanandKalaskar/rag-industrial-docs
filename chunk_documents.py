 # chunk_documents.py
# Step 2 of RAG: Split pages into smaller, searchable chunks

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

# --- Load documents (same as before) ---
docs_folder = "C:\D\Rag\documents"
all_documents = []

for filename in os.listdir(docs_folder):
    if filename.endswith(".pdf"):
        filepath = os.path.join(docs_folder, filename)
        loader = PyPDFLoader(filepath)
        all_documents.extend(loader.load())

print(f"Loaded: {len(all_documents)} pages")

# --- Chunk the documents ---
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,       # Each chunk is roughly 500 characters (~100 words)
    chunk_overlap=50,     # Chunks overlap by 50 characters so we don't cut mid-sentence
    separators=["\n\n", "\n", ". ", " "]  # Try to split at paragraph breaks first, then sentences
)

chunks = splitter.split_documents(all_documents)

print(f"Split into: {len(chunks)} chunks (before filtering)")

# --- Filter out tiny useless chunks ---
min_chunk_length = 150  # Chunks under 100 characters are usually headers, page numbers, junk
chunks = [c for c in chunks if len(c.page_content.strip()) >= min_chunk_length]

print(f"After filtering: {len(chunks)} meaningful chunks")

# --- See what chunks look like now ---
print("\n--- Chunk 0 ---")
print(f"Source: {chunks[0].metadata['source']}")
print(f"Page: {chunks[0].metadata['page']}")
print(f"Length: {len(chunks[0].page_content)} characters")
print(f"Content:\n{chunks[0].page_content}")

print("\n--- Chunk 10 ---")
print(f"Source: {chunks[10].metadata['source']}")
print(f"Page: {chunks[10].metadata['page']}")
print(f"Length: {len(chunks[10].page_content)} characters")
print(f"Content:\n{chunks[10].page_content}")