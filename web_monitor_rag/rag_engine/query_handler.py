
from web_monitor_rag.rag_engine.embedder import embed_text
from web_monitor_rag.storage import chroma_connector
import requests

PROMPT_TEMPLATE = """
You are a helpful assistant. Use the following context to answer the user's question.

Context:
{context}

Question: {question}
Answer:
"""

GEMMA_API_URL = "http://localhost:11434/"  # Adjust if endpoint is different

def ask_gemma(prompt, max_tokens=256):
    response = requests.post(
        GEMMA_API_URL,
        json={"prompt": prompt, "max_tokens": max_tokens}
    )
    response.raise_for_status()
    # Adjust this if your API returns a different structure
    return response.json().get("response", response.text)

def query_rag(user_query, top_k=3):
    query_emb = embed_text(user_query)[0]
    results = chroma_connector.get_collection().query(
        query_embeddings=[query_emb],
        n_results=top_k
    )
    docs = results['documents'][0]
    metadatas = results['metadatas'][0]
    context = "\n---\n".join([f"[{m.get('site', '')}] {d}" for d, m in zip(docs, metadatas)])
    prompt = PROMPT_TEMPLATE.format(context=context, question=user_query)
    return {
        'prompt': prompt,
        'results': list(zip(docs, metadatas))
    }

if __name__ == '__main__':
    # Example usage
    user_query = input("Enter your question: ")
    rag_result = query_rag(user_query)
    prompt = rag_result['prompt']
    print("\nPrompt sent to Gemma:\n", prompt)
    answer = ask_gemma(prompt)
    print("\nGemma's answer:\n", answer)
