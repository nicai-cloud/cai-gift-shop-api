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
    
    async def send_email_to_customer(self, to_email: str, customer_info: dict, order_info: dict):
        # Create the email
        email = Mail(
            from_email=get("FROM_EMAIL"),
            to_emails=to_email
        )

        email.template_id = "d-0d5368d2d8e2456a88c1f7d48b648b1e"

        email.dynamic_template_data = {
            "orderNumber": order_info["order_number"],
            "orderTotal": order_info["total_cost"],
            "preselectionItems": order_info["ordered_items"]["preselection_items"],
            "customItems": order_info["ordered_items"]["custom_items"],
            "firstName": customer_info["first_name"],
            "lastName": customer_info["last_name"],
            "mobile": customer_info["mobile"],
            "email": customer_info["email"]
        }

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
