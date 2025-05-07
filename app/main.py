from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .routers import auth

app = FastAPI()
app.include_router(auth.router, prefix="/api", tags=["auth"])
origins = [
    "http://127.0.0.1:5173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
