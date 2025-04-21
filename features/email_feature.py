import boto3
import logging
import os
import certifi
from uuid import UUID
import sendgrid
from sendgrid.helpers.mail import Mail
from api.types import Customer
from api.request_types import CustomerInfoRequest
from utils.format_number import format_number

from utils.config import get

LOG = logging.getLogger(__name__)

os.environ["SSL_CERT_FILE"] = certifi.where()
sg = sendgrid.SendGridAPIClient(api_key=get("SENDGRID_API_KEY"))

ses = boto3.client('ses', region_name='ap-southeast-2')

class EmailFeature:
    def __init__(self):
        super().__init__()
    
    # Use SendGrid, which has a limit of 100 email per day, to send order confirmation email to customer
    async def send_order_confirmation_email_to_customer(self, customer_info: CustomerInfoRequest, order_info: dict, fulfillment_method: int):
        # Create the email
        email = Mail(
            from_email=get("FROM_EMAIL"),
            to_emails=customer_info.email
        )

        if fulfillment_method == 0: # Pickup
            email.template_id = get("PICKUP_ORDER_CONFIRMATION_EMAIL_TEMPLATE_ID")

            template_data = {
                "orderNumber": order_info["order_number"],
                "subtotal": f'${format_number(order_info["subtotal"])}',
                "orderTotal": f'${format_number(order_info["order_total"])}',
                "preselectionItems": order_info["ordered_items"]["preselection_items"],
                "customItems": order_info["ordered_items"]["custom_items"],
                "firstName": customer_info.first_name,
                "lastName": customer_info.last_name,
                "mobile": customer_info.mobile,
                "email": customer_info.email
            }
        else:   # Delivery
            email.template_id = get("ORDER_CONFIRMATION_EMAIL_TEMPLATE_ID")

            template_data = {
                "orderNumber": order_info["order_number"],
                "subtotal": f'${format_number(order_info["subtotal"])}',
                "shippingCost": "Free" if order_info["shipping_cost"] == 0 else f'${format_number(order_info["shipping_cost"])}',
                "orderTotal": f'${format_number(order_info["order_total"])}',
                "preselectionItems": order_info["ordered_items"]["preselection_items"],
                "customItems": order_info["ordered_items"]["custom_items"],
                "firstName": customer_info.first_name,
                "lastName": customer_info.last_name,
                "mobile": customer_info.mobile,
                "email": customer_info.email
            }

            # Only append subtotalAfterDiscount if there is a discount
            if order_info["subtotal_after_discount"] < order_info["subtotal"]:
                template_data.update({
                    "subtotalAfterDiscount": f'${format_number(order_info["subtotal_after_discount"])}'
                })

        email.dynamic_template_data = template_data

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
