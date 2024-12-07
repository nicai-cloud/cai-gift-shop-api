import logging
import os
import certifi
from uuid import UUID
import sendgrid
from sendgrid.helpers.mail import Mail

from utils.config import get

LOG = logging.getLogger(__name__)

os.environ["SSL_CERT_FILE"] = certifi.where()
sg = sendgrid.SendGridAPIClient(api_key=get("SENDGRID_API_KEY"))

class EmailFeature:
    def __init__(self):
        super().__init__()
    
    async def send_email(self, to_email: str, order_id: UUID):
        # Create the email
        email = Mail(
            from_email=get("FROM_EMAIL"),
            to_emails=to_email,
            subject='Successful order',
            html_content=f"<strong>Thanks for your purchase, your order id is {order_id}!</strong>"
        )

        # Send the email
        try:
            response = sg.send(email)
            print(f"Email sent! Status code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
