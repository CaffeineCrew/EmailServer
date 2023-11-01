from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException

from server.core.ConfigEnv import config

from fastapi_mail import ConnectionConfig, FastMail
# import resend

app = FastAPI(title="Techdocs",
              version="V0.0.1",
              description="API for automatic code documentation generation!"
              )

from server import router

try:
    conf = ConnectionConfig(
        MAIL_USERNAME=config.MAIL_USERNAME,
        MAIL_PASSWORD=config.MAIL_PASSWORD,
        MAIL_FROM=config.MAIL_FROM,
        MAIL_PORT=2525,
        MAIL_SERVER="smtp.gmail.com",
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        TEMPLATE_FOLDER="server/templates",
        USE_CREDENTIALS = True,
        VALIDATE_CERTS = True
        
        # MAIL_TLS=True,
        # MAIL_SSL=False
    )

    app.state.mail_client = FastMail(conf)

    # resend.api_key = "re_eJBe5r89_31AU33Tjrrb7RYgh5n7z15q5"

except Exception as e:
    print(e)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while initializing mail client")
