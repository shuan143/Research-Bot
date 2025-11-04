import os
import requests
from dotenv import load_dotenv
import time

load_dotenv()
#i use the opensource api key
API_KEY = os.getenv("API_KEY")

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def query_llm(prompt):
    payload = {
        "model": "mistralai/mistral-7b-instruct:free",  # 公開模型
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    content = response.json()
    return content

if __name__ == "__main__":
    print("=== 🤖 Public LLM (OpenRouter) ===\n")
    while True:
        q = input("Ask something (or type 'exit'): ")
        time.sleep(1)
        if q.lower() == "exit":
            break
        print("\n🧠 Thinking...")
        cont=query_llm(q)
        print(cont['choices'][0]['message']['content'])
        print("\nresponse provider:", cont['provider'])
        print("model url:", f"https://openrouter.ai/api/v1/chat/completions/{cont['model']}")
        print("\n==============================================\n")
