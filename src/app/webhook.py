from fastapi import APIRouter, Request
from ..groupme_bot import GroupMeBot
from src.database.mongodb_client import MongodbClient

router = APIRouter()
bot = GroupMeBot()
db = MongodbClient()

def get_user(group_id):
    user = list(db.get_collection('config', {'admin_group_id': group_id}))
    print(user)
    return user if len(user) > 0 else None

@router.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()
    print("Received payload:", payload)

    sender_type = payload.get("sender_type", "")
    if sender_type == "bot":
        return {"status": "ignored"}

    message_text = payload.get('text', '')
    sender_name = payload.get("name", "Unknown")

    if message_text.startswith("/need_approval"):
        user = get_user(payload.get('group_id', ''))

        if user:
            request_text = message_text.replace("/need_approval", "").strip()
            bot.pending_approval_message = request_text
            admin_names = bot.get_admin_name(user[0]['admin_group_id'], user[0]['user_name'])
            print(admin_names)

            approval_request = (
                f"**Approval Needed**\n"
                f"👤 @{sender_name} requested approval.\n\n"
                f'Message: "{request_text}"\n\n'
                f'👤 @{admin_names[0]}\n'
                '✅ Reply with `/approve` to send.\n'
                '❌ Reply with `/reject` to deny.'
            )
            bot.send_message(user[0], approval_request)
            return {"status": "approval requested"}
        return {"status": "user not found"}

    if bot.pending_approval_message:
        user = get_user(payload.get('group_id', ''))
        if user:
            if sender_name in bot.get_admin_name(user[0]['admin_group_id'], user[0]['user_name']):
                if message_text.startswith("/approve"):
                    bot.send_message(user[0], 'Message approved and sent to all groups.')
                    bot.send_message_to_groups(user[0])
                    bot.pending_approval_message = ''
                    return {"status": "message sent"}
                elif message_text.startswith("/reject"):
                    bot.send_message(user[0], "Message rejected.")
                    bot.pending_approval_message = ''
                    return {"status": "message rejected"}
                return {"status": "pending approval"}
        return {"status": "user not found"}
    
    return {'status': 'no request'}
