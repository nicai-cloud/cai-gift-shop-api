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
    
    async def send_email_to_customer(self, to_email: str, order_number: str):
        # Create the email
        email = Mail(
            from_email=get("FROM_EMAIL"),
            to_emails=to_email,
            subject='Successful order',
            html_content=f"<strong>Thanks for your purchase, your order number is {order_number}</strong>"
        )

        # Send the email
        try:
            response = sg.send(email)
            print(f"Email sent! Status code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")

    async def send_email_to_me(self, customer_id: UUID, order_number: str, order_id: UUID):
        # Create the email
        email = Mail(
            from_email=get("FROM_EMAIL"),
            to_emails=get("FROM_EMAIL"),
            subject='Successful order',
            html_content=f"<strong>Customer {customer_id} has placed an order with order number {order_number} and order id {order_id}!</strong>"
        )

        # Send the email
        try:
            response = sg.send(email)
            print(f"Email sent! Status code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
