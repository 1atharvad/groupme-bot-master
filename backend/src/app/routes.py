import os
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()
frontend_path = os.path.abspath(os.path.join(os.getcwd(), "../frontend/dist/index.html"))

@router.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    return FileResponse(frontend_path)