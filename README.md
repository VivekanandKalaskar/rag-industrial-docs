 # 🔧 RAG Pipeline for Industrial Documentation

A production-style Retrieval-Augmented Generation (RAG) system that enables natural language querying over 50+ industrial safety and maintenance documents. Built with LangChain, ChromaDB, and Sentence Transformers.

## Problem

Industrial organizations maintain hundreds of safety manuals, maintenance guides, and compliance documents. Finding specific information across these documents is slow, error-prone, and requires deep familiarity with the document library. Traditional keyword search fails when users phrase questions differently from the source text.

## Solution

This system uses semantic search and LLM-powered generation to let users ask questions in plain English and receive accurate, source-cited answers drawn directly from the document library.

## Architecture
User Question
│
▼
┌─────────────┐
│  Streamlit   │
│     UI       │
└──────┬──────┘
│
▼
┌─────────────┐     ┌──────────────────┐
│   Embedding  │────▶│    ChromaDB       │
│    Model     │     │  Vector Store     │
│ (MiniLM-L6) │     │  (6,612 chunks)   │
└─────────────┘     └────────┬─────────┘
│ Top-k results
▼
┌──────────────────┐
│   LLM (Mistral/  │
│   GPT/NVIDIA)    │
│                  │
│  Context + Query │
│  → Cited Answer  │
└──────────────────┘

## Key Features

- **Semantic Search**: Finds relevant content by meaning, not just keywords
- **Source Citations**: Every answer references specific documents and page numbers
- **Multi-Document**: Processes and searches across 50+ industrial PDFs simultaneously
- **Model-Agnostic**: Works with local models (Ollama), NVIDIA NIM, or OpenAI — swap with a config change
- **Persistent Storage**: Vector store persists to disk — no re-embedding on restart
- **Chat Interface**: Conversational UI with full chat history

## Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Framework | LangChain | RAG pipeline orchestration |
| Vector DB | ChromaDB | Embedding storage & similarity search |
| Embeddings | Sentence Transformers (all-MiniLM-L6-v2) | Text → 384-dim vector conversion |
| LLM | NVIDIA NIM / Ollama (Phi-3) / OpenAI | Answer generation |
| Document Processing | PyPDF | PDF text extraction |
| Text Splitting | RecursiveCharacterTextSplitter | Intelligent document chunking |
| Frontend | Streamlit | Interactive web interface |

## How It Works

1. **Document Ingestion**: PDFs are loaded and text is extracted page by page
2. **Chunking**: Pages are split into ~500 character chunks with 50 char overlap using recursive splitting (paragraph → sentence → word boundaries)
3. **Filtering**: Chunks under 150 characters (headers, page numbers) are removed to reduce noise
4. **Embedding**: Each chunk is converted to a 384-dimensional vector using Sentence Transformers
5. **Storage**: Vectors are stored in ChromaDB with source metadata (filename, page number)
6. **Retrieval**: User queries are embedded and the top-4 most similar chunks are retrieved
7. **Generation**: Retrieved chunks are passed as context to the LLM with a structured prompt
8. **Citation**: The LLM is instructed to reference specific sources in its answer

## Setup

### Prerequisites
- Python 3.10+
- Ollama (for local LLM) or NVIDIA NIM API key

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/rag-industrial-docs.git
cd rag-industrial-docs
pip install -r requirements.txt
```

### For local LLM (free, no API key):
```bash
# Install Ollama from https://ollama.com
ollama pull phi3:mini
```

### Run

```bash
# Download industrial documents
python download_docs.py

# Build vector store
python build_vectorstore.py

# Launch the app
streamlit run app.py
```

## Project Structure

rag-industrial-docs/
├── app.py                  # Streamlit web interface
├── rag_pipeline.py         # Core RAG logic (CLI version)
├── build_vectorstore.py    # Document processing & embedding pipeline
├── download_docs.py        # OSHA document downloader
├── download_more.py        # Extended document collection
├── test_llm.py             # LLM connection test
├── test_embeddings.py      # Embedding similarity demo
├── requirements.txt        # Python dependencies
├── documents/              # PDF document library (50+ files)
└── chroma_db/              # Persisted vector store

## Sample Queries

- "What are the steps to conduct a job hazard analysis?"
- "What are the requirements for confined space entry?"
- "How should employers handle hazardous chemical exposure?"
- "What personal protective equipment is required for welding?"

## Design Decisions

- **Chunk size 500 chars**: Balances retrieval precision (smaller = more focused) against context coherence (larger = more complete). Tested 300, 500, and 800 — 500 performed best on industrial Q&A.
- **150 char minimum filter**: Eliminates title pages, headers, and footers that add noise to search results.
- **Top-4 retrieval**: Provides enough context for comprehensive answers without overwhelming the LLM's context window.
- **Model-agnostic design**: Started with local Ollama for zero-cost development, added NVIDIA NIM for production quality. Architecture supports any OpenAI-compatible endpoint.

## Future Enhancements

- Hybrid search (BM25 + semantic) with cross-encoder re-ranking
- Evaluation framework measuring faithfulness and context recall
- Pinecone integration for cloud-hosted vector storage
- Multi-format support (DOCX, HTML, spreadsheets)