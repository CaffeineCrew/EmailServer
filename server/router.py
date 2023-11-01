from fastapi import Request, Depends, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from server import app

import resend

from .models import *
from .services import *

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/send",tags=["mail"])
def send_email(bgtasks: BackgroundTasks, details: EmailSchema):
    # await ops_send_email(bgtasks, details)
    r = resend.Emails.send({
  "from": "onboarding@resend.dev",
  "to": details.recipients[0],
  "subject": "Techdocs",
  "HTML": f'''<a href="{details.template_kwargs['verify_link']}">link</a><p>Congrats on sending your <strong>first email</strong>!</p>'''
})

