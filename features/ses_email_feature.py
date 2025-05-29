import boto3
import logging
from uuid import UUID
from utils.config import get

LOG = logging.getLogger(__name__)

ses = boto3.client('ses', region_name='ap-southeast-2')


class SESEmailFeature:
    def __init__(self):
        super().__init__()

    async def send_email_to_me(self, first_name: str, last_name: str, customer_id: UUID, order_number: str, order_id: UUID):
        # Send the email
        try:
            body = f"Customer {first_name} {last_name} of id {customer_id} has placed an order with order number {order_number} and order id {order_id}!"

            response = ses.send_email(
                Source=get("FROM_EMAIL"),
                Destination={
                    'ToAddresses': [get("TO_EMAIL")],
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