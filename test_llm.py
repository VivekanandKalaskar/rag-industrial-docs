# test_nvidia.py
# Test NVIDIA NIM API connection

from langchain_openai import ChatOpenAI

# NVIDIA NIM uses the same OpenAI-compatible format
llm = ChatOpenAI(
    model="openai/gpt-oss-20b",
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

# Same question we asked Phi-3
question = "What are three common causes of centrifugal pump failure?"
print("Asking NVIDIA NIM...\n")

response = llm.invoke(question)
print(response.content)