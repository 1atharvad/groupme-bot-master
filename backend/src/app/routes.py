import os
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/{page_name}.{ext}")
async def serve_txt(page_name: str, ext: str):
    frontend_path = os.path.abspath(os.path.join(os.getcwd(), f"../frontend/dist/{page_name}.{ext}"))
    return FileResponse(frontend_path)

@router.get("/{page_name}")
async def serve_html(page_name: str):
    frontend_path = os.path.abspath(os.path.join(os.getcwd(), f"../frontend/dist/{page_name}.html"))
    return FileResponse(frontend_path)

@router.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    frontend_path = os.path.abspath(os.path.join(os.getcwd(), "../frontend/dist/index.html"))
    return FileResponse(frontend_path)