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
    print(f"🔍 Searching Google: {query}\n")
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
    prompt += " If this question requires recent or factual data, reply with only the word 'yes'. Otherwise, just answer directly."
    payload = {
        "model": "mistralai/mistral-7b-instruct:free",  # 公開模型
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    content = response.json()

    # get model reply content
    reply = content['choices'][0]['message']['content'].strip().lower()
    if reply == "yes":
        #ask model what keyword it wants to search
        prompt2 = "give me what you want to search('just key word')"
        payload2 = {
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": [
                {"role": "user", "content": prompt2}
            ]
        }
        response2 = requests.post(url, headers=headers, json=payload2)
        response2.raise_for_status()
        keyword = response2.json()['choices'][0]['message']['content'].strip()

        #search web
        result = google_sereach(keyword)

        #ask model to summarize search result
        summary_prompt = f"Summarize concisely and accurately based on the following web search results:\n{result}"
        payload3 = {
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": [
                {"role": "user", "content": summary_prompt}
            ]
        }
        response3 = requests.post(url, headers=headers, json=payload3)
        response3.raise_for_status()
        return response3.json()

    return content

if __name__ == "__main__":
    print("=== 🤖 Public LLM (OpenRouter) ===\n")
    while True:
        q = input("Ask something (or type 'exit'): ")
        time.sleep(1)
        if q.lower() == "exit":
            break
        print("\n🧠 Thinking...")
        cont = query_llm(q)
        print(cont['choices'][0]['message']['content'])
        print("\nresponse provider:", cont.get('provider', 'unknown'))
        print("model url:", f"https://openrouter.ai/models/{cont['model']}")
        print("\n==============================================\n")