 # test_embeddings.py
# Understanding embeddings: how text becomes searchable by meaning

from langchain_huggingface import HuggingFaceEmbeddings

# Load embedding model — runs locally, free, no API needed
# This model is specifically trained to make similar sentences have similar vectors
print("Loading embedding model (first time takes 1-2 minutes to download)...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Let's see what an embedding looks like
text = "How to prevent electrical accidents in the workplace"
vector = embeddings.embed_query(text)

print(f"\nText: '{text}'")
print(f"Vector length: {len(vector)} dimensions")
print(f"First 10 numbers: {vector[:10]}")

# Now the magic — similar texts get similar vectors
texts = [
    "Ensure proper grounding of all electrical equipment",  # Related
    "Wear insulated gloves when working with live wires",   # Related
    "How to make a chocolate cake from scratch",            # Not related
]

print("\n--- Similarity Demo ---")
question_vector = embeddings.embed_query(text)

for t in texts:
    t_vector = embeddings.embed_query(t)
    
    # Calculate similarity (dot product — higher = more similar)
    similarity = sum(a * b for a, b in zip(question_vector, t_vector))
    print(f"\nCompared to: '{t}'")
    print(f"Similarity score: {similarity:.4f}")