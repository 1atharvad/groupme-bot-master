from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .groupme_bot import GroupMeBot

app = FastAPI()   
bot = GroupMeBot()
templates = Jinja2Templates(directory="src/templates")
app.mount("/src/static", StaticFiles(directory="src/static"), name="static")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("pages/home.jinja", {"request": request})

@app.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()
    print("Received payload:", payload)

    sender_type = payload.get("sender_type", "")
    if sender_type == "bot":
        return {"status": "ignored"}

    message_text = payload.get('text', '')
    sender_name = payload.get("name", "Unknown")

    if message_text.startswith("/need_approval"):
        request_text = message_text.replace("/need_approval", "").strip()
        bot.pending_approval_message = request_text

        approval_request = (
            f"**Approval Needed**\n"
            f"👤 @{sender_name} requested approval.\n\n"
            f'Message: "{request_text}"\n\n'
            f'👤 @{bot.admin_group_admin[0]}\n'
            '✅ Reply with `/approve` to send.\n'
            '❌ Reply with `/reject` to deny.'
        )
        bot.send_message(approval_request)
        return {"status": "approval requested"}

    if bot.pending_approval_message and sender_name in bot.admin_group_admin:
        if message_text.startswith("/approve"):
            bot.send_message('Message approved and sent to all groups.')
            bot.send_message_to_groups()
            bot.pending_approval_message = ''
            return {"status": "message sent"}
        elif message_text.startswith("/reject"):
            bot.send_message("Message rejected.")
            bot.pending_approval_message = ''
            return {"status": "message rejected"}
        return {"status": "pending approval"}
    
    return {'status': 'no request'}
