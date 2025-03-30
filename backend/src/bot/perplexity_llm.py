import requests
import os
import re
import json
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
PERPLEXITY_API_TOKEN = os.getenv('PERPLEXITY_API_TOKEN')
MODEL = os.getenv('MODEL')

class QueryResponseFormat(BaseModel):
    message_text: str

class PerplexityAPI:
    def __init__(self):
        self.url = 'https://api.perplexity.ai/chat/completions'
        self.headers = {
            'Authorization': f'Bearer {PERPLEXITY_API_TOKEN}',
            'Content-Type': 'application/json'
        }

    def get_query_response(self, query: str, additional_prompt='') -> str:
        system_prompt = """
            You are an AI assistant who will check the grammar and improve the text provided.
            """
        
        user_prompt = f'''
            check the grammar and improve the text provided, do not change the meaning or idea of the sentences provided
            do not provide any other information, just provide the improved version

            Output Rules:
            - Return results strictly in JSON format.
            - The JSON object must contain the following fields: improved_data
            - {additional_prompt}

            Query: "{query}"
            '''
        
        response = requests.request('POST', self.url, json={
            'model': MODEL,
            'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt},
            ],
            "temperature": 0.5,
            'search_recency_filter': 'day',
        }, headers=self.headers)

        if response.status_code == 200:
            data = json.loads(response.text)['choices'][0]['message']['content']
            match = re.search(r'json\s*(.*?)\s*', data, re.DOTALL)

            if match:
                cleaned_string = re.sub(r'```json\n|\n```', '', data)
                return json.loads(cleaned_string)
        return None
    
if __name__ == '__main__':
    llm = PerplexityAPI()
    query_str = 'I like to go to vacation to Canada, I will like to visit Itay'
    additional_prompt = 'Add emojis'
    print(llm.get_query_response(query_str, additional_prompt))
