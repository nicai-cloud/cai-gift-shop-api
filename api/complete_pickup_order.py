from falcon import HTTPBadRequest, HTTPError, HTTP_OK

from api.base import RequestHandler, route
from api.request_types import CompletePickupOrderRequest, OrderItemsRequest
from api.response_types import CalculateSubtotalResponse, CompleteOrderResponse
from features.payment_method_feature import PaymentMethodFeature
from features.customer_feature import CustomerFeature
from features.resend_email_feature import ResendEmailFeature
from features.ses_email_feature import SESEmailFeature
from features.order_feature import OrderFeature
from features.order_item_feature import OrderItemFeature
from features.preselection_feature import PreselectionFeature
from features.inventory_feature import InventoryFeature
from features.coupon_feature import CouponFeature
from infrastructure.work_management import WorkManager

import marshmallow


class CompletePickupOrderRequestHandler(RequestHandler):
    def __init__(self, work_manager: WorkManager):
        super().__init__()
        self.customer_feature = CustomerFeature(work_manager)
        self.order_item_feature = OrderItemFeature(work_manager)
        self.order_feature = OrderFeature(work_manager)
        self.preselection_feature = PreselectionFeature(work_manager)
        self.inventory_feature = InventoryFeature(work_manager)
        self.payment_method_feature = PaymentMethodFeature()
        self.resend_email_feature = ResendEmailFeature()
        self.ses_email_feature = SESEmailFeature()
        self.coupon_feature = CouponFeature(work_manager)

    @route.post("/calculate-subtotal", auth_exempt=True)
    async def calculate_subtotal(self, req, resp):
        raw_request_body = await req.get_media()
        print('request_body', raw_request_body)

        try:
            request_body = OrderItemsRequest.Schema().load(raw_request_body)
        except marshmallow.exceptions.ValidationError as e:
            raise HTTPBadRequest(title="Invalid request payload", description=str(e))

        order_items = request_body.order_items
        subtotal, subtotal_after_discount = await self.order_feature.calculate_subtotal(order_items=order_items)
        resp.media = CalculateSubtotalResponse(subtotal=subtotal, subtotal_after_discount=subtotal_after_discount)
        resp.status = HTTP_OK

    @route.post("/", auth_exempt=True)
    async def complete_order(self, req, resp):
        raw_request_body = await req.get_media()
        print('request_body', raw_request_body)

        try:
            request_body = CompletePickupOrderRequest.Schema().load(raw_request_body)
        except marshmallow.exceptions.ValidationError as e:
            raise HTTPBadRequest(title="Invalid request payload", description=str(e))

        customer_info = request_body.customer_info
        order_items = request_body.order_items
        fulfillment_method = request_body.fulfillment_method

        first_name = customer_info.first_name
        last_name = customer_info.last_name
        # TODO: sanitisation on email and mobile
        email = customer_info.email
        mobile = customer_info.mobile

        # Check if there are enough stocks
        ordered_bag_quantities, ordered_item_quantities = await self.order_feature.calculate_order_quantities(order_items)
        stocks_available = await self.inventory_feature.check_stock_availability(ordered_bag_quantities, ordered_item_quantities)
        if not stocks_available:
            raise HTTPError(status="400", description="Out of stock")
        
        # Calculate subtotal and make the payment
        subtotal, subtotal_after_discount = await self.order_feature.calculate_subtotal(order_items, 0)
        shipping_cost = await self.order_feature.calculate_shipping_cost(fulfillment_method, subtotal)
        order_total = round(subtotal_after_discount + shipping_cost, 2)

        # If the code reaches here, it means the payment is successful, then we update inventories
        await self.inventory_feature.update_inventories(ordered_bag_quantities, ordered_item_quantities)
        
        # Create customer
        customer_id = await self.customer_feature.create_customer(first_name, last_name, email, mobile)
        print('!! created customer id:', customer_id)

        # Create an order against the customer
        order_id, order_number = await self.order_feature.create_order(
            customer_id=customer_id,
            subtotal=subtotal,
            discount=None,
            subtotal_after_discount=None,
            shipping_cost=shipping_cost,
            fulfillment_method=fulfillment_method,
            delivery_address=None,
            coupon_id=None
        )
        print('!! created order id:', order_id)

        # Create each of the order items
        order_item_ids = []
        for order_item in order_items:
            quantity = order_item.quantity
            preselection_id = order_item.preselection_id
            bag_id = order_item.bag_id
            item_ids = order_item.item_ids

            order_item_id = await self.order_item_feature.create_order_item(quantity, preselection_id, bag_id, item_ids, order_id)
            order_item_ids.append(order_item_id)
            print('!! created order item id:', order_item_id)

        order_info = await self.order_feature.generate_order_info(order_number, order_items, subtotal, subtotal_after_discount, shipping_cost, order_total)

        # Send the successful order email to customer and myself
        await self.resend_email_feature.send_order_confirmation_email(customer_info, order_info, fulfillment_method)
        await self.ses_email_feature.send_email_to_me(first_name, last_name, customer_id, order_number, order_id)

        resp.media = CompleteOrderResponse(order_number=order_number)
        resp.status = HTTP_OK
