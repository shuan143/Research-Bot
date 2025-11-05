import os
import requests
from dotenv import load_dotenv
import time
from googleapiclient.discovery import build

load_dotenv()
#i use the opensource api key
API_KEY = os.getenv("API_KEY")
GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def google_sereach(query, num_results=5):
    print(print(f"🔍 Searching Google: {query}\n"))
    try:
        #build the service
        service = build("customsearch", "v1", developerKey=GOOGLE_SEARCH_API_KEY)

        #excute search
        result = service.cse().list(
            q=query,
            cx=GOOGLE_CSE_ID,
            num=num_results
        ).execute()
        return result
    except Exception as e:
        print(f"❌ Search error: {e}")
        return []

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
        print("\n=======================================================\n")
        print("which you want to ask():")
        print("web_search(\"web\") or LLM(\"llm\") or quit(\"quit\")")
        choose = input()
        if choose.lower()=="llm":
            while True:
                q = input("Ask something (or type \'exit\'): ")
                time.sleep(1)
                if q.lower() == "exit":
                    break
                print("\n🧠 Thinking...")
                cont=query_llm(q)
                print(cont['choices'][0]['message']['content'])
                print("\nresponse provider:", cont['provider'])
                print("model url:", f"https://openrouter.ai/api/v1/chat/completions/{cont['model']}")
                print("\n==============================================\n")
        elif choose.lower()=="web":
            q = input("Enter what you want to search(or type \'exit\'): ")
            if q.lower() == "exit":
                break
            responses = google_sereach(q)
            responses = responses['items']
            counter=0
            for item in responses:
                print(f"{counter}.{item['title']}")
                print("   snippet: ", item['snippet'])
                print("   url: ", item['link'], "\n")

        elif choose.lower()=="quit":
            break
