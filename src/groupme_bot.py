import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_ID = os.getenv("GROUPME_BOT_ID")
ACCESS_TOKEN = os.getenv("GROUPME_ACCESS_TOKEN")
ADMIN_GROUP_ID = os.getenv("ADMIN_GROUP_ID")
TARGET_BOT_NAME = os.getenv('TARGET_BOT_NAME')
TARGET_GROUP_IDS = os.getenv("TARGET_GROUP_IDS").split(",")
CALLBACK_URL = os.getenv('CALLBACK_URL')

class GroupMeBot:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(GroupMeBot, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.pending_approval_message = ''
        self.api_url = 'https://api.groupme.com/v3'
        self.admin_group_admin = self.get_admin_name(ADMIN_GROUP_ID)

    def get_bot_details(self, bot_name: str, group_ids: str|list):
        url = f"{self.api_url}/bots"
        response = requests.get(url, params={"token": ACCESS_TOKEN})
        
        if response.status_code == 200:
            bots = response.json().get("response", [])
            if type(group_ids) == str:
                bots = list(filter(lambda bot: bot['group_id'] == group_ids and bot['name'] == bot_name, bots))
                return bots[0] if len(bots) > 0 else None
            else:
                return list(filter(lambda bot: bot['group_id'] in group_ids and bot['name'] == bot_name, bots))
        else:
            return None

    def create_bot(self, bot_name: str, group_id: str):
        bot = self.get_bot_details(bot_name, group_id)

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
            response = requests.post(url, json=data, headers=headers, params={"token": ACCESS_TOKEN})
            return response.json()
        else:
            return bot

    def send_message_to_groups(self, message=''):
        """Send a message to a specific GroupMe group using the group_id."""
        message = message if message else self.pending_approval_message
        bot_ids = [bot_details['bot_id'] for bot_details in self.get_bot_details(TARGET_BOT_NAME, TARGET_GROUP_IDS)]

        for bot_id in bot_ids:
            url = f"{self.api_url}/bots/post"
            payload = {
                "bot_id": bot_id,
                "text": message
            }
            requests.post(url, json=payload)

    def send_message(self, message: str):
        url = f"{self.api_url}/bots/post"
        payload = {
            "bot_id": BOT_ID,
            "text": message
        }
        requests.post(url, json=payload)

    def get_group_members(self, group_id):
        """Fetch the members of a GroupMe group."""
        url = f"{self.api_url}/groups/{group_id}"
        response = requests.get(url, params={"token": ACCESS_TOKEN})
        
        if response.status_code == 200:
            return response.json()['response']['members']
        else:
            return None

    def get_admin_name(self, group_id):
        admins = []
        
        for member in self.get_group_members(group_id):
            if 'admin' in member['roles']:
                admins.append(member['name'])
        return admins
    
if __name__ == '__main__':
    bot = GroupMeBot()
    # print(bot.create_bot(TARGET_BOT_NAME, '106602750'))
    print([bot_details['bot_id'] for bot_details in bot.get_bot_details(TARGET_BOT_NAME, TARGET_GROUP_IDS)])
    # print(bot.get_group_members('106602737'))