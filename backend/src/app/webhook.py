from fastapi import APIRouter, Request
from src.bot.perplexity_llm import PerplexityAPI
from src.bot.groupme_bot import GroupMeBot
from src.database.mongodb_client import MongodbClient

router = APIRouter()
bot = GroupMeBot()
db = MongodbClient()
llm = PerplexityAPI()

class GroupBotMessageSystem:
    _instance = None

    def __new__(cls, payload):
        if cls._instance is None:
            cls._instance = super(GroupBotMessageSystem, cls).__new__(cls)
        return cls._instance

    def __init__(self, payload):
        if not hasattr(self, "pending_approval_message"):
            self.pending_approval_message = {}
        if not hasattr(self, "request_type"):
            self.request_type = ''
        self.payload = payload
        self.user = self.get_user(payload.get('group_id', ''))
        self.message_text = payload.get('text', '')
        self.sender_name = payload.get("name", "Unknown")

    def get_user(self, group_id):
        user = list(db.get_collection('config', {'admin_group_id': group_id}))
        return user if len(user) > 0 else None
    
    def get_pending_approval_message(self):
        if self.user:
            return self.pending_approval_message.get(self.user[0]['user_name'], '')
        return ''
    
    def set_pending_approval_message(self, message):
        if self.user:
            self.pending_approval_message[self.user[0]['user_name']] = message
    
    def handle_system(self):
        if self.message_text == "/help":
            return self.handle_help()
        elif self.message_text.startswith("/need_approval"):
            return self.send_approval_request()
        elif self.message_text == "/status":
            return self.send_status()

        if self.user:
            if self.get_pending_approval_message():
                if self.request_type == 'approval':
                    return self.handle_approval()
                elif self.request_type == 'improve':
                    return self.handle_improve_with_llm()
                

    def handle_help(self):
        if self.user:
            help_message = (
                "🤖 **GroupMe Chatbot Commands** 🤖\n"
                "✅ `/help` - Show available commands\n"
                "✅ `/need_approval <message_text>` - Sends the message to be approved\n"
                "✅ `/improve <message_text>` - Sends the message for improvement using AI\n"
                "✅ `/improve` - Sends the previous message for improvement using AI\n"
                "✅ `/cancel` - Cancels the current message thread, removing the complete message.\n"
                "✅ `/need_approval` - Sends the previous message to be approved\n"
                "✅ `/approve - Admin approves the message for forwarding to all target groups\n"
                "✅ `/reject` - Reject the message, no further action needed\n"
                "✅ `/status` - Check bot status\n"
            )
            bot.send_message(self.user, help_message)
            return {"status": "help message sent"}
        return {"status": "user not found"}
    
    def send_status(self):
        if self.user:
            status_message = "✅ The bot is running and responding to commands!"
            bot.send_message(self.user, status_message)
            return {"status": "bot working"}
        return {"status": "user not found"}
    
    def improve_message(self):
        if self.user:
            self.request_type = 'improve'
            request_text = self.message_text.replace("/improve", "").strip()

            if request_text == '':
                request_text = self.get_pending_approval_message()
            request_text = llm.get_query_response(request_text).get('improved_data', '')
            self.set_pending_approval_message(request_text)


            improve_request = (
                f"**Improve using AI**\n"
                f"👤 @{self.sender_name} has requested an improvement.\n\n"
                f'Message: "{self.get_pending_approval_message()}"\n\n'
                '✅ Reply with `/need_approval` to send the message for approval.\n'
                '✍️ Reply with `/improve` for further improvements.\n'
                '❌ Reply with `/cancel` to cancel the current message thread.'
            )
            bot.send_message(self.user, improve_request)
            return {"status": "message improved"}
        return {"status": "user not found"}
    
    def handle_improve_with_llm(self):
        if self.user:
            if self.sender_name in bot.get_admin_name(self.user[0]['admin_group_id'], self.user[0]['user_name']):
                if self.message_text == "/need_approval":
                    return self.send_approval_request()
                elif self.message_text == "/improve":
                    return self.improve_message()
                elif self.message_text.startswith("/cancel"):
                    self.request_type = ''
                    bot.send_message(self.user, "Message removed.")
                    self.set_pending_approval_message('')
                    return {"status": "message removed"}
                return {"status": "pending approval"}
        return {"status": "user not found"}

    def send_approval_request(self):
        if self.user:
            self.request_type = 'approval'
            admin_names = bot.get_admin_name(self.user[0]['admin_group_id'], self.user[0]['user_name'])
            request_text = self.message_text.replace("/need_approval", "").strip()

            if request_text == '':
                request_text = self.get_pending_approval_message()
            self.set_pending_approval_message(request_text)

            approval_request = (
                f"**Approval Needed**\n"
                f"👤 @{self.sender_name} requested approval.\n\n"
                f'Message: "{self.get_pending_approval_message()}"\n\n'
                f'👤 @{admin_names[0]}\n'
                '✅ Reply with `/approve` to send.\n'
                '❌ Reply with `/reject` to deny.'
            )
            bot.send_message(self.user, approval_request)
            return {"status": "approval requested"}
        return {"status": "user not found"}

    def handle_approval(self):
        if self.user:
            if self.sender_name in bot.get_admin_name(self.user[0]['admin_group_id'], self.user[0]['user_name']):
                if self.message_text.startswith("/approve"):
                    self.request_type = ''
                    bot.send_message(self.user, 'Message approved and sent to all groups.')
                    bot.send_message_to_groups(self.user, self.get_pending_approval_message())
                    self.set_pending_approval_message('')
                    return {"status": "message sent"}
                elif self.message_text.startswith("/reject"):
                    self.request_type = ''
                    bot.send_message(self.user, "Message rejected.")
                    self.set_pending_approval_message('')
                    return {"status": "message rejected"}
                return {"status": "pending approval"}
        return {"status": "user not found"}

@router.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()
    sender_type = payload.get("sender_type", "")

    if sender_type == "bot":
        return {"status": "ignored"}
    
    message_system = GroupBotMessageSystem(payload)
    message_system.handle_system()

    return {'status': 'no request'}
