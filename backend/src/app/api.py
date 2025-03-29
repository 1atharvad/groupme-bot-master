from bson import json_util
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.bot.groupme_bot import GroupMeBot
from src.database.mongodb_client import MongodbClient

router = APIRouter()
db = MongodbClient()
bot = GroupMeBot()

class ClientIdRequest(BaseModel):
    user_name: str
    client_id: str

class BotDetailsRequest(BaseModel):
    _id: str
    user_name: str
    bot_name: str
    group_id: str
    group_name: str
    type: str
    bot_status: str

@router.get("/api/get-client-id/{username}")
async def getClientId(username: str):
    try:
        userlist = list(db.get_collection('config', {'user_name': username}))
        client_id = userlist[0]['client_id'] if len(userlist) > 0 else None

        if client_id is None:
            raise HTTPException(status_code=404, detail="Client ID not found")
        return JSONResponse({"client_id": client_id})
    except HTTPException as http_e:
        raise http_e
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.post("/api/set-client-id")
async def getClientId(request_data: ClientIdRequest):
    try:
        db.add_to_collection('config', request_data)
        return JSONResponse({"message": "Client ID set successfully"})
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.get("/api/get-group-ids/{username}")
async def getGroupIds(username: str):
    try:
        group_ids = bot.get_all_group_ids(username)
        if group_ids is None:
            raise HTTPException(status_code=404, detail="Group IDs not found")
        return JSONResponse({"group_ids": group_ids})
    except HTTPException as http_e:
        raise http_e
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.get("/api/get-bot-groups/{username}")
async def getGroupForBot(username: str):
    try:
        admin_group = list(map(lambda group: {key: val if key != "_id" else str(val) for key, val in group.items()},
                               db.get_collection('groups', {'user_name': username, 'type': 'admin_group'})))
        target_groups = list(map(lambda group: {key: val if key != "_id" else str(val) for key, val in group.items()},
                                 db.get_collection('groups', {'user_name': username, 'type': 'target_groups'})))
        return JSONResponse(json_util.loads(json_util.dumps({"admin_group": admin_group, "target_groups": target_groups})))
    except HTTPException as http_e:
        raise http_e
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.post("/api/set-bot-groups")
async def createGroupForBot(request_data: BotDetailsRequest):    
    try:
        request_dict = request_data.model_dump()
        response = db.add_to_collection('groups', request_dict)

        if response.acknowledged:
            request_dict['_id'] = str(response.inserted_id)
            bot.create_bot(request_dict['user_name'], request_dict['bot_name'], request_dict['group_id'])
            return JSONResponse(request_dict)
        else:
            raise HTTPException(status_code=500, detail="Failed to insert document")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.put("/api/update-bot-groups/{id}")
async def updateGroupForBot(id: str, request_data: BotDetailsRequest):    
    try:
        request_dict = request_data.model_dump()
        bot_details = list(db.get_collection('groups', {'_id': id}))[0]
        response = db.update_collection('groups', {'_id': id}, request_dict)

        if response.acknowledged:
            if bot_details['bot_name'] != request_dict['bot_name']:
                bot.update_bot(request_dict['user_name'], bot_details['bot_name'], bot_details['group_id'], request_dict['bot_name'])
            if bot_details['group_name'] != request_dict['group_name']:
                bot.delete_bot(request_dict['user_name'], bot_details['bot_name'], bot_details['group_id'])
                bot.create_bot(request_dict['user_name'], request_dict['bot_name'], request_dict['group_id'])
            request_dict['_id'] = str(id)
            return JSONResponse(request_dict)
        else:
            raise HTTPException(status_code=500, detail="Failed to update document")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.delete("/api/delete-bot-group/{id}")
async def deleteGroupBot(id: str):    
    try:
        bot_details = list(db.get_collection('groups', {'_id': id}))[0]
        response = db.delete_collection('groups', {'_id': id})

        if response.acknowledged:
            bot.delete_bot(bot_details['user_name'], bot_details['bot_name'], bot_details['group_id'])
            return JSONResponse({'message': 'Group details deleted'})
        else:
            raise HTTPException(status_code=500, detail="Failed to delete the document")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")