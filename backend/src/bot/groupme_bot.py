import os
import requests
from dotenv import load_dotenv
from src.database.mongodb_client import MongodbClient

load_dotenv()

CALLBACK_URL = os.getenv('CALLBACK_URL')
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME= os.getenv('DB_NAME')

db = MongodbClient()

class GroupMeBot:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(GroupMeBot, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.api_url = 'https://api.groupme.com/v3'

    def get_all_group_ids(self, username):
        url = f"{self.api_url}/groups"
        user = list(db.get_collection('config', {'user_name': username}))

        if len(user) > 0:
            response = requests.get(url, params={"token": user[0]['access_token']})

            return [{
                'id': group_details['group_id'],
                'name': group_details['name'],
                'admins': [{
                    'user_id': member['user_id'],
                    'name': member['name']
                    } for member in filter(lambda x: 'admin' in x['roles'], group_details['members'])]
                } for group_details in response.json()['response']]
        return None

    def get_bot_details(self, bot_name: str|list, group_ids: str|list, username: str ='', user: any = None):
        url = f"{self.api_url}/bots"
        if username:
            user = list(db.get_collection('config', {'user_name': username}))

        if user and len(user) > 0:
            response = requests.get(url, params={"token": user[0]['access_token']})
            
            if response.status_code == 200:
                bots = response.json().get("response", [])
                if type(group_ids) == str and type(bot_name) == str:
                    bots = list(filter(lambda bot: bot['group_id'] == group_ids and bot['name'] == bot_name, bots))
                    return bots[0] if len(bots) > 0 else None
                else:
                    return list(filter(lambda bot: bot['group_id'] in group_ids and bot['name'] in bot_name, bots))
        return None

    def create_bot(self, username: str, bot_name: str, group_id: str):
        bot = self.get_bot_details(bot_name, group_id, username=username)

        if not bot:
            url = f"{self.api_url}/bots"
            headers = {"Content-Type": "application/json"}
            data = {
                "bot": {
                    "name": bot_name,
                    "group_id": group_id,
                    "callback_url": CALLBACK_URL,
                    "dm_notification": False
                }
            }
            user = list(db.get_collection('config', {'user_name': username}))
            response = requests.post(url, json=data, headers=headers, params={"token": user[0]['access_token']})
            return response.json()
        else:
            return bot
        
    def update_bot(self, username: str, bot_name: str, group_id: str, new_name: str):
        bot = self.get_bot_details(bot_name, group_id, username=username)

        if bot:
            url = f"{self.api_url}/bots/update"
            headers = {"Content-Type": "application/json"}
            data = {
                "bot": {
                    "bot_id": bot['bot_id'],
                    "name": new_name
                }
            }
            user = list(db.get_collection('config', {'user_name': username}))
            response = requests.post(url, json=data, headers=headers, params={"token": user[0]['access_token']})
            
            if response.status_code == 200:
                return {"message": "Bot updated successfully!"}
            else:
                return {"error": f"Failed to update bot: {response.text}"}
        else:
            return {"error": "Bot not found!"}
        
    def delete_bot(self, username: str, bot_name: str, group_id: str):
        bot = self.get_bot_details(bot_name, group_id, username=username)

        if bot:
            url = f"{self.api_url}/bots/destroy"
            headers = {"Content-Type": "application/json"}
            data = {
                "bot_id": bot['bot_id']
            }
            user = list(db.get_collection('config', {'user_name': username}))
            response = requests.post(url, json=data, headers=headers, params={"token": user[0]['access_token']})
            
            if response.status_code == 200:
                return {"message": "Bot deleted successfully!"}
            else:
                return {"error": f"Failed to delete bot: {response.text}"}
        else:
            return {"error": "Bot not found!"}

    def send_message_to_groups(self, user, message=''):
        """Send a message to a specific GroupMe group using the group_id."""
        target_bot_details = db.get_target_bot_details(user[0]['user_name'])

        if target_bot_details:
            bot_details = self.get_bot_details(target_bot_details['bot_names'], target_bot_details['group_ids'], user=user)

            if bot_details:
                for bot_details in bot_details:
                    url = f"{self.api_url}/bots/post"
                    payload = {
                        "bot_id": bot_details['bot_id'],
                        "text": message
                    }
                    requests.post(url, json=payload)

    def send_message(self, user, message: str):
        url = f"{self.api_url}/bots/post"
        admin_bot_details = db.get_admin_bot_details(user[0]['user_name'])

        if admin_bot_details:
            bot_details = self.get_bot_details(admin_bot_details['bot_name'], admin_bot_details['group_id'], user=user)

            if bot_details:
                payload = {
                    "bot_id": bot_details['bot_id'],
                    "text": message
                }
            requests.post(url, json=payload)

    def get_group_members(self, group_id, username):
        """Fetch the members of a GroupMe group."""
        url = f"{self.api_url}/groups/{group_id}"
        user = list(db.get_collection('config', {'user_name': username}))

        if len(user) > 0:
            response = requests.get(url, params={"token": user[0]['access_token']})
            
            if response.status_code == 200:
                return response.json()['response']['members']
        return None

    def get_admin_name(self, group_id, username):
        admins = []
        
        for member in self.get_group_members(group_id, username):
            if 'admin' in member['roles']:
                admins.append(member['name'])
        return admins
    
if __name__ == '__main__':
    bot = GroupMeBot()