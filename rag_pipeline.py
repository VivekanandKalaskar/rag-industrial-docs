# rag_pipeline.py
# The complete RAG pipeline: Question → Search → Generate answer with sources

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
import chromadb

# --- Connect to our existing vector store ---
print("Loading vector store...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="chroma_db")

vectorstore = Chroma(
    client=client,
    collection_name="industrial_docs",
    embedding_function=embeddings
)

print(f"Loaded {vectorstore._collection.count()} vectors")

# --- Connect to NVIDIA NIM ---
llm = ChatOpenAI(
    model="openai/gpt-oss-20b",
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="your-nvidia-api-key"
)

# --- The RAG function ---
def ask(question):
    # Step 1: Search for relevant chunks
    results = vectorstore.similarity_search_with_score(question, k=4)

    # Step 2: Build context from search results
    context_parts = []
    sources = []

    for i, (doc, score) in enumerate(results):
        context_parts.append(f"[Source {i+1}]: {doc.page_content}")
        source_file = doc.metadata['source'].split('\\')[-1]
        sources.append(f"Source {i+1}: {source_file}, Page {doc.metadata['page']}")

    context = "\n\n".join(context_parts)

    # Step 3: Create the prompt
    prompt = f"""You are an industrial safety expert. Answer the question based ONLY on the 
provided context. If the context doesn't contain enough information, say so.
Always reference which source(s) you used in your answer.

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""

    # Step 4: Get LLM response
    response = llm.invoke(prompt)

    # Step 5: Print everything
    print(f"\n{'='*60}")
    print(f"QUESTION: {question}")
    print(f"{'='*60}")
    print(f"\nANSWER:\n{response.content}")
    print(f"\n{'='*60}")
    print("SOURCES USED:")
    for s in sources:
        print(f"  {s}")
    print(f"{'='*60}")

# --- Try it ---
ask("What are the steps to conduct a job hazard analysis?")
ask("How to prevent electrical hazards in the workplace?")