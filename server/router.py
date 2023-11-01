from fastapi import Request, Depends, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from server import app

from .models import *
from .services import *

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://caffeinecrew-techdocs.hf.space", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/send",tags=["mail"])
def send_email(bgtasks: BackgroundTasks, details: EmailSchema, ):
    await ops_send_email(bgtasks, details)
