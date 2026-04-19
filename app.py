 # app.py
# RAG Pipeline for Industrial Documentation — Streamlit Interface

import streamlit as st
import os
import chromadb
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI

# --- Page Config ---
st.set_page_config(
    page_title="Industrial RAG Assistant",
    page_icon="🔧",
    layout="wide"
)

st.title("🔧 Industrial Documentation RAG Assistant")
st.caption("Ask questions about industrial safety documents — answers are sourced directly from uploaded PDFs")

# --- Sidebar: Settings & Document Upload ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    api_key = st.text_input("NVIDIA NIM API Key", type="password")
    
    st.divider()
    st.header("📄 Documents")
    
    uploaded_files = st.file_uploader(
        "Upload PDF documents",
        type="pdf",
        accept_multiple_files=True
    )
    
    # Save uploaded files to documents folder
    docs_folder = "documents"
    os.makedirs(docs_folder, exist_ok=True)
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            filepath = os.path.join(docs_folder, uploaded_file.name)
            if not os.path.exists(filepath):
                with open(filepath, "wb") as f:
                    f.write(uploaded_file.getbuffer())
    
    # Count existing documents
    existing_pdfs = [f for f in os.listdir(docs_folder) if f.endswith(".pdf")]
    st.info(f"📁 {len(existing_pdfs)} documents in library")
    
    # Build / Rebuild vector store button
    build_clicked = st.button("🔨 Build Vector Store", use_container_width=True)


# --- Initialize Components (cached so they load only once) ---
@st.cache_resource
def load_embeddings():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def build_vectorstore(docs_folder, embeddings):
    """Load PDFs, chunk, embed, store in ChromaDB"""
    all_documents = []
    
    for filename in os.listdir(docs_folder):
        if filename.endswith(".pdf"):
            filepath = os.path.join(docs_folder, filename)
            loader = PyPDFLoader(filepath)
            all_documents.extend(loader.load())
    
    if not all_documents:
        return None, 0
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " "]
    )
    chunks = splitter.split_documents(all_documents)
    chunks = [c for c in chunks if len(c.page_content.strip()) >= 150]
    
    # Clear old data and rebuild
    db_path = "chroma_db"
    client = chromadb.PersistentClient(path=db_path)
    
    # Delete existing collection if it exists
    try:
        client.delete_collection("industrial_docs")
    except Exception:
        pass
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        client=client,
        collection_name="industrial_docs"
    )
    
    return vectorstore, len(chunks)


def load_existing_vectorstore(embeddings):
    """Load an already-built vector store from disk"""
    db_path = "chroma_db"
    if not os.path.exists(db_path):
        return None
    
    client = chromadb.PersistentClient(path=db_path)
    vectorstore = Chroma(
        client=client,
        collection_name="industrial_docs",
        embedding_function=embeddings
    )
    
    if vectorstore._collection.count() == 0:
        return None
    
    return vectorstore


# --- Load embeddings ---
embeddings = load_embeddings()

# --- Handle vector store building ---
if build_clicked:
    with st.spinner("Building vector store... This may take a minute."):
        vectorstore, chunk_count = build_vectorstore(docs_folder, embeddings)
        if vectorstore:
            st.session_state["vectorstore_ready"] = True
            st.sidebar.success(f"✅ Built with {chunk_count} chunks")
        else:
            st.sidebar.error("No PDFs found in documents folder")

# --- Load existing vector store ---
vectorstore = load_existing_vectorstore(embeddings)


# --- RAG Function ---
def ask_question(question, vectorstore, api_key):
    """Run the full RAG pipeline"""
    
    # Search
    results = vectorstore.similarity_search_with_score(question, k=4)
    
    # Build context
    context_parts = []
    sources = []
    
    for i, (doc, score) in enumerate(results):
        context_parts.append(f"[Source {i+1}]: {doc.page_content}")
        source_file = doc.metadata['source'].split('\\')[-1].split('/')[-1]
        sources.append({
            "file": source_file,
            "page": doc.metadata['page'],
            "score": score,
            "content": doc.page_content[:200]
        })
    
    context = "\n\n".join(context_parts)
    
    # Prompt
    prompt = f"""You are an industrial safety expert. Answer the question based ONLY on the 
provided context. If the context doesn't contain enough information, say so.
Always reference which source(s) you used in your answer.

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""
    
    # Generate
    llm = ChatOpenAI(
        model="openai/gpt-oss-20b",
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key
    )
    
    response = llm.invoke(prompt)
    
    return response.content, sources


# --- Main Chat Interface ---
if vectorstore is None:
    st.warning("👈 Upload documents and click 'Build Vector Store' to get started.")
elif not api_key:
    st.warning("👈 Enter your NVIDIA NIM API key in the sidebar.")
else:
    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "sources" in message:
                with st.expander("📎 Sources"):
                    for s in message["sources"]:
                        st.markdown(f"**{s['file']}** — Page {s['page']} (relevance: {s['score']:.3f})")
                        st.caption(s["content"] + "...")
    
    # Chat input
    if question := st.chat_input("Ask a question about your industrial documents..."):
        # Show user message
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
        
        # Generate answer
        with st.chat_message("assistant"):
            with st.spinner("Searching documents and generating answer..."):
                answer, sources = ask_question(question, vectorstore, api_key)
                st.markdown(answer)
                with st.expander("📎 Sources"):
                    for s in sources:
                        st.markdown(f"**{s['file']}** — Page {s['page']} (relevance: {s['score']:.3f})")
                        st.caption(s["content"] + "...")
        
        # Save to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": sources
        })