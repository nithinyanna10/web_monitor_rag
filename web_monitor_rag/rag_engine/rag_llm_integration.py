import requests
from web_monitor_rag.rag_engine.query_handler import query_rag

MODEL_NAME = "gemma3:27b-it-qat"
GEMMA_API_URL = "http://localhost:11434/api/chat"

def ask_gemma(prompt):
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(GEMMA_API_URL, json=payload, stream=True)
    response.raise_for_status()
    answer = ""
    for line in response.iter_lines():
        if line:
            try:
                part = line.decode("utf-8")
                import json
                data = json.loads(part)
                answer += data.get("message", {}).get("content", "")
            except Exception:
                continue
    return answer

if __name__ == "__main__":
    user_query = input("Enter your question: ")
    rag_result = query_rag(user_query)
    prompt = rag_result['prompt']
    print("\nPrompt sent to Gemma:\n", prompt)
    answer = ask_gemma(prompt)
    print("\nGemma's answer:\n", answer) 