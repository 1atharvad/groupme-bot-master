import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .api import router as api_router
from .routes import router as template_router
from .webhook import router as webhook_router

app = FastAPI()

frontend_path = os.path.abspath(os.path.join(os.getcwd(), "../frontend/dist/_next/static"))
app.mount("/_next/static", StaticFiles(directory=frontend_path), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.include_router(template_router)
app.include_router(webhook_router)

__all__ = ['app']