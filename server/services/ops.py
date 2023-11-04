from fastapi import HTTPException, BackgroundTasks

from fastapi_mail import MessageSchema, MessageType

from server import app

# import resend
import ElasticEmail
import glob
import pprint
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
        if "server/templates/"+details.template_name not in template_names:
            raise HTTPException(status_code=400, detail="Template name not found")
        
        with open (f"server/templates/{details.template_name}", "r") as f:
            template = f.read().format(**details.template_kwargs)

        # message = resend.Emails.send({
        #     "from": "onboarding@resend.dev",
        #     "to": f"{details.recipients[0]}",
        #     "subject": f"{details.subject}",
        #     "html": f"{template}"
        # })


        # message = MessageSchema(
        #     subject=details.subject,
        #     recipients=details.recipients,  # List of recipients, as many as you can pass
        #     template_body=details.template_kwargs,
        #     subtype=MessageType.html
        # )
        with ElasticEmail.ApiClient(app.state.elastic_email_config) as api_client:
            api_instance = emails_api.EmailsApi(api_client)
            email_message_data = EmailMessageData(
                recipients=[
                    EmailRecipient(
                        email=details.recipients[0]
                    ),
                ],
                content={
        	    "Body": [
        		{
        		    "ContentType":"HTML",
        		    "Content":f'<a href="{details.template_kwargs.get('verify_link'}">Link</a>'
        		}
        	    ],
        	    "Subject": details.subject,
        	    "From": config.EMAIL_FROM
        	}
            )
         
            try:
                api_response = api_instance.emails_post(email_message_data)
                pprint(api_response)
                return api_response
            except ElasticEmail.ApiException as e:
                print("Exception when calling EmailsApi->emails_post: %s\n" % e)

        # bgtasks.add_task(app.state.mail_client.send_message, message=message, template_name=details.template_name)
        # await app.state.mail_client.send_message(message=message, template_name=details.template_name)
    
    else:
        message = MessageSchema(
            subject=details.subject,
            recipients=details.recipients,  # List of recipients, as many as you can pass
            body=details.body,
            subtype=MessageType.html
        )

        # bgtasks.add_task(app.state.mail_client.send_message, message=message)
        await app.state.mail_client.send_message(message=message)
        
        

        
        

