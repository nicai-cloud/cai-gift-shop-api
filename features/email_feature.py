import boto3
import logging
import os
import certifi
from uuid import UUID
import sendgrid
from sendgrid.helpers.mail import Mail
from api.types import Customer

from utils.config import get

LOG = logging.getLogger(__name__)

os.environ["SSL_CERT_FILE"] = certifi.where()
sg = sendgrid.SendGridAPIClient(api_key=get("SENDGRID_API_KEY"))

ses = boto3.client('ses', region_name='ap-southeast-2')

class EmailFeature:
    def __init__(self):
        super().__init__()
    
    # Use SendGrid, which has a limit of 100 email per day, to send order confirmation email to customer
    async def send_order_confirmation_email_to_customer(self, to_email: str, customer_info: dict, order_info: dict):
        # Create the email
        email = Mail(
            from_email=get("FROM_EMAIL"),
            to_emails=to_email
        )

        email.template_id = get("ORDER_CONFIRMATION_EMAIL_TEMPLATE_ID")

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
    
    # Use SendGrid, which has a limit of 100 email per day, to send delivery email to customer
    async def send_delivery_email_to_customer(self, customer: Customer, tracking_number: str):
        # Create the email
        email = Mail(
            from_email=get("FROM_EMAIL"),
            to_emails=customer.email
        )

        email.template_id = get("DELIVERY_EMAIL_TEMPLATE_ID")

        email.dynamic_template_data = {
            "firstName": customer.first_name,
            "lastName": customer.last_name,
            "address": customer.address,
            "trackingNumber": tracking_number
        }

        # Send the email
        try:
            response = sg.send(email)
            print(f"Email sent! Status code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")

    # Use SES, which has a much larger limit of 62,000 email per month, to send email to myself
    async def send_email_to_me(self, customer_id: UUID, order_number: str, order_id: UUID):
        # Send the email
        try:
            body = f"Customer {customer_id} has placed an order with order number {order_number} and order id {order_id}!"

            response = ses.send_email(
                Source=get("FROM_EMAIL"),
                Destination={
                    'ToAddresses': [get("FROM_EMAIL")],
                },
                Message={
                    'Subject': {
                        'Data': 'New order placed'
                    },
                    'Body': {
                        'Text': {
                            'Data': body
                        }
                    }
                }
            )
            print("Email sent! Message ID:", response['MessageId'])
        except Exception as e:
            print(f"Error: {e}")
