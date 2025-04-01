import os
import certifi
import requests
import json
from bson import ObjectId
from requests.auth import HTTPDigestAuth
from dotenv import load_dotenv
from pymongo import MongoClient
from pydantic import BaseModel

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
PROJECT_ID = os.getenv('PROJECT_ID')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
PUBLIC_KEY = os.getenv('PUBLIC_KEY')
DB_NAME= os.getenv('DB_NAME')

class MongodbClient:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(MongodbClient, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.access_list_url = f'https://cloud.mongodb.com/api/atlas/v1.0/groups/{PROJECT_ID}/accessList'
        self.ip_whitelist_comment = f'Added programmatically ({"dev" if self.is_dev_server() else (prod)})'
        self.whitelist_ip()
        self.client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())

    @staticmethod
    def is_dev_server():
        return os.getenv("FASTAPI_ENV") == "development"
    
    @staticmethod
    def get_current_ip():
        response = requests.get('https://api64.ipify.org?format=json')
        return response.json()['ip']
    
    def get_whitelisted_ips(self):
        response = requests.get(
            self.access_list_url,
            auth=HTTPDigestAuth(PUBLIC_KEY, PRIVATE_KEY)
        )
        return response.json() if response.status_code == 200 else None
    
    def remove_ips(self, ip_list):
        for ip in ip_list:
            requests.delete(
                f'{self.access_list_url}/{ip}',
                auth=HTTPDigestAuth(PUBLIC_KEY, PRIVATE_KEY)
            )

    def whitelist_ip(self):
        ip = self.get_current_ip()
        filtered_ip_details = filter(
            lambda ip_details: ip_details['comment'] == self.ip_whitelist_comment,
            self.get_whitelisted_ips()['results']
        )
        ip_list = list(map(lambda ip_details: ip_details['ipAddress'], filtered_ip_details))

        if ip not in ip_list:
            self.remove_ips(ip_list)
            self.add_new_ip(ip)

    def add_new_ip(self, ip):
        response = requests.post(
            self.access_list_url,
            auth=HTTPDigestAuth(PUBLIC_KEY, PRIVATE_KEY),
            headers={'Content-Type': 'application/json'},
            data=json.dumps([{'ipAddress': ip, 'comment': self.ip_whitelist_comment}])
        )
        return response.json()

    def get_admin_bot_details(self, username):
        admin_group = list(self.get_collection('groups', {'user_name': username, 'type': 'admin_group'}))

        if len(admin_group) > 0:
            return {
                'bot_name': admin_group[0]['bot_name'],
                'group_id': admin_group[0]['group_id']
            }
        return None
    
    def get_target_bot_details(self, username):
        target_groups = list(self.get_collection('groups', {'user_name': username, 'type': 'target_groups'}))
        target_bot_details = {
            'bot_names': [],
            'group_ids': []
        }

        for group in target_groups:
            target_bot_details['bot_names'].append(group['bot_name'])
            target_bot_details['group_ids'].append(group['group_id'])
        return target_bot_details

    def get_collection(self, collection_name, filter_query={}):
        if '_id' in filter_query:
            filter_query['_id'] = ObjectId(filter_query['_id'])

        return self.client[DB_NAME][collection_name].find(filter_query)
    
    def add_to_collection(self, collection_name, data: list | dict):
        if isinstance(data, list):
            return self.client[DB_NAME][collection_name].insert_many(data)
        elif isinstance(data, BaseModel):
            return self.client[DB_NAME][collection_name].insert_one(data.model_dump())
        elif isinstance(data, dict):
            return self.client[DB_NAME][collection_name].insert_one(data)

    def update_collection(self, collection_name, filter_query, data: dict):
        if '_id' in filter_query:
            filter_query['_id'] = ObjectId(filter_query['_id'])

        if isinstance(data, BaseModel):
            return self.client[DB_NAME][collection_name].update_one(filter_query, {"$set": data.model_dump()})
        else:
            return self.client[DB_NAME][collection_name].update_one(filter_query, {"$set": data})
        
    def delete_collection(self, collection_name, filter_query):
        if '_id' in filter_query:
            filter_query['_id'] = ObjectId(filter_query['_id'])

        return self.client[DB_NAME][collection_name].delete_one(filter_query)
    
if __name__ == '__main__':
    client = MongodbClient()
    print(client.get_current_ip())
    print(client.get_collection('config')[0]['client_id'])