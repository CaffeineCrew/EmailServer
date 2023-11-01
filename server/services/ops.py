from fastapi import HTTPException, BackgroundTasks

from fastapi_mail import MessageSchema, MessageType

from server import app

import glob
from server.models import *
from server.core.ConfigEnv import config

def ops_send_email(bgtasks: BackgroundTasks, details: EmailSchema):
    if details.body is None and details.template_name is None:
        raise HTTPException(status_code=400, detail="Either body or template_name must be specified")
    
    
    
    if details.recipients and isinstance(details.recipients, str):
        details.recipients = [details.recipients]

    elif details.recipients is None:
        details.recipients = [config.MAIL_FROM] 
    
    
    
    if details.template_name is not None:
        template_names = glob.glob("server/templates/*.html")
        if "server/templates\\"+details.template_name not in template_names:
            raise HTTPException(status_code=400, detail="Template name not found")
        
        message = MessageSchema(
            subject=details.subject,
            recipients=details.recipients,  # List of recipients, as many as you can pass
            template_body=details.template_kwargs,
            subtype=MessageType.html
        )

        bgtasks.add_task(app.state.mail_client.send_message, message=message, template_name=details.template_name)
    
    else:
        message = MessageSchema(
            subject=details.subject,
            recipients=details.recipients,  # List of recipients, as many as you can pass
            body=details.body,
            subtype=MessageType.html
        )

        bgtasks.add_task(app.state.mail_client.send_message, message=message)
        

        
        

