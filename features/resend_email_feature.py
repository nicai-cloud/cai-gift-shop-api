import logging
import resend
from dataclasses import asdict
from jinja2 import Environment, FileSystemLoader

from api.types import Customer, OrderInfo
from api.request_types import CustomerInfoRequest
from utils.config import get
from utils.format_number import format_number

LOG = logging.getLogger(__name__)

resend.api_key = get("RESEND_API_KEY")


class ResendEmailFeature:
    def __init__(self):
        super().__init__()
        self.env = Environment(loader=FileSystemLoader("utils"))

    async def _generate_pickup_order_content(self, customer_info: CustomerInfoRequest, order_info: OrderInfo):
        template = self.env.get_template("email_templates/pickup_order_confirmation.html")

        template_data = {
            "orderNumber": order_info.order_number,
            "subtotal": f'${format_number(order_info.subtotal)}',
            "orderTotal": f'${format_number(order_info.order_total)}',
            "preselectionItems": [asdict(preselection_item) for preselection_item in order_info.ordered_items.preselection_items],
            "customItems": [asdict(custom_item) for custom_item in order_info.ordered_items.custom_items],
            "firstName": customer_info.first_name,
            "lastName": customer_info.last_name,
            "mobile": customer_info.mobile,
            "email": customer_info.email
        }

        # Render template with dynamic data
        return template.render(**template_data)

    async def _generate_delivery_order_content(self, customer_info: CustomerInfoRequest, order_info: OrderInfo):
        template = self.env.get_template("email_templates/delivery_order_confirmation.html")

        template_data = {
            "orderNumber": order_info.order_number,
            "subtotal": f'${format_number(order_info.subtotal)}',
            "shippingCost": "Free" if order_info.shipping_cost == 0 else f'${format_number(order_info.shipping_cost)}',
            "orderTotal": f'${format_number(order_info.order_total)}',
            "preselectionItems": [asdict(preselection_item) for preselection_item in order_info.ordered_items.preselection_items],
            "customItems": [asdict(custom_item) for custom_item in order_info.ordered_items.custom_items],
            "firstName": customer_info.first_name,
            "lastName": customer_info.last_name,
            "mobile": customer_info.mobile,
            "email": customer_info.email
        }

        # Only append subtotalAfterDiscount if there is a discount
        if order_info.subtotal_after_discount < order_info.subtotal:
            template_data.update({
                "subtotalAfterDiscount": f'${format_number(order_info.subtotal_after_discount)}'
            })

        # Render template with dynamic data
        return template.render(**template_data)

    async def _generate_delivery_order_in_transit_content(self, customer: Customer, delivery_address: str, tracking_number: str):
        template = self.env.get_template("email_templates/delivery_order_in_transit.html")

        template_data = {
            "firstName": customer.first_name,
            "lastName": customer.last_name,
            "address": delivery_address,
            "trackingNumber": tracking_number
        }

        # Render template with dynamic data
        return template.render(**template_data)

    async def _generate_pickup_order_ready_for_pickup_content(self, customer: Customer, order_number: str):
        template = self.env.get_template("email_templates/pickup_order_ready_for_pickup.html")

        template_data = {
            "orderNumber": order_number,
            "firstName": customer.first_name,
            "lastName": customer.last_name,
            "pickupAddress": get("PICKUP_ADDRESS"),
        }

        # Render template with dynamic data
        return template.render(**template_data)

    async def send_order_confirmation_email(self, customer_info: CustomerInfoRequest, order_info: OrderInfo, fulfillment_method: int):
        if fulfillment_method == 0: # Pickup
            html_content = await self._generate_pickup_order_content(customer_info, order_info)
        else:   # Delivery
            html_content = await self._generate_delivery_order_content(customer_info, order_info)

        params = {
            "from": get("FROM_EMAIL"),
            "to": [customer_info.email],
            "subject": "ORDER CONFIRMATION",
            "html": html_content,
        }

        response = resend.Emails.send(params)
        print(f"Email sent with id: {response['id']}")

    async def send_delivery_order_in_transit_email(self, customer: Customer, delivery_address: str, tracking_number: str):
        html_content = await self._generate_delivery_order_in_transit_content(customer, delivery_address, tracking_number)

        params = {
            "from": get("FROM_EMAIL"),
            "to": [customer.email],
            "subject": "ORDER CONFIRMATION",
            "html": html_content,
        }

        response = resend.Emails.send(params)
        print(f"Email sent with id: {response['id']}")

    async def send_pickup_order_ready_for_pickup_email(self, customer: Customer, order_number: str):
        html_content = await self._generate_pickup_order_ready_for_pickup_content(customer, customer, order_number)

        params = {
            "from": get("FROM_EMAIL"),
            "to": [customer.email],
            "subject": "ORDER CONFIRMATION",
            "html": html_content,
        }

        response = resend.Emails.send(params)
        print(f"Email sent with id: {response['id']}")
