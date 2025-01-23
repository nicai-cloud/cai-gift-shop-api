from falcon import HTTPBadRequest, HTTPError, HTTP_OK

from api.base import RequestHandler, route
from api.input_types import CompleteOrderInput
from api.types import PublishableKeyResponse
from features.payment_method_feature import PaymentMethodFeature
from features.customer_feature import CustomerFeature
from features.email_feature import EmailFeature
from features.order_feature import OrderFeature
from features.order_item_feature import OrderItemFeature
from features.preselection_feature import PreselectionFeature
from features.inventory_feature import InventoryFeature
from features.coupon_feature import CouponFeature
from infrastructure.work_management import WorkManager
from utils.config import get


class CompleteOrderRequestHandler(RequestHandler):
    def __init__(self, work_manager: WorkManager):
        super().__init__()
        self.customer_feature = CustomerFeature(work_manager)
        self.order_item_feature = OrderItemFeature(work_manager)
        self.order_feature = OrderFeature(work_manager)
        self.preselection_feature = PreselectionFeature(work_manager)
        self.inventory_feature = InventoryFeature(work_manager)
        self.payment_method_feature = PaymentMethodFeature()
        self.email_feature = EmailFeature()
        self.coupon_feature = CouponFeature(work_manager)

    @route.post("/calculate-subtotal", auth_exempt=True)
    async def calculate_subtotal(self, req, resp):
        request_body = await req.get_media()
        print('request_body', request_body)

        order_items = request_body["order_items"]
        resp.media = await self.order_feature.calculate_subtotal(order_items=order_items)
    
    @route.get("/publishable-key", auth_exempt=True)
    async def get_publishable_key(self, req, resp):
        resp.media = PublishableKeyResponse(
            publishable_key=get("STRIPE_PUBLISHABLE_KEY"),
        )

    @route.post("/", auth_exempt=True)
    async def complete_order(self, req, resp):
        raw_request_body = await req.get_media()
        print('request_body', raw_request_body)

        request_body = CompleteOrderInput.Schema().load(raw_request_body)
        print("!!!", request_body)

        customer_info = request_body.customer_info
        order_items = request_body.order_items
        shipping_method = request_body.shipping_method
        payment_method_id = request_body.payment_method_id
        coupon_code = request_body.coupon_code

        first_name = customer_info.first_name
        last_name = customer_info.last_name
        # TODO: sanitisation on email and mobile
        email = customer_info.email
        mobile = customer_info.mobile
        address = customer_info.address

        # Check if the coupon code is valid
        if coupon_code is None:
            coupon = None
        else:
            coupon = await self.coupon_feature.get_coupon_by_code(coupon_code)
            if coupon is None:
                raise HTTPBadRequest(
                    title="invalid coupon code",
                    description="The provided coupon_code is invalid."
                )

        # Check if there are enough stocks
        bag_quantities, item_quantities = await self.order_feature.calculate_order_quantities(order_items)
        stocks_available = await self.inventory_feature.check_stock_availability(bag_quantities, item_quantities)
        if not stocks_available:
            raise HTTPError(status="400", description="Out of stock")
        
        # Calculate subtotal and make the payment
        subtotal, subtotal_after_discount = await self.order_feature.calculate_subtotal(order_items, coupon.discount_percentage if coupon else 0)
        discount = round(subtotal - subtotal_after_discount, 2)
        shipping_cost = await self.order_feature.calculate_shipping_cost(shipping_method, subtotal)
        order_total = subtotal_after_discount + shipping_cost
        await self.payment_method_feature.create_payment_intent(payment_method_id, order_total)

        # If the code reaches here, it means the payment is successful, then we update inventories
        await self.inventory_feature.update_inventories(bag_quantities, item_quantities)
        
        # Create customer
        customer_id = await self.customer_feature.create_customer(first_name, last_name, email, mobile, address)
        print('!! created customer id:', customer_id)

        # Create an order against the customer
        order_id, order_number = await self.order_feature.create_order(
            customer_id=customer_id,
            subtotal=subtotal,
            discount=discount if coupon else None,
            subtotal_after_discount=subtotal_after_discount if coupon else None,
            shipping_cost=shipping_cost,
            shipping_method=shipping_method,
            coupon_id=coupon.id if coupon else None
        )
        print('!! created order id:', order_id)

        # Mark the coupon as used
        if coupon:
            await self.coupon_feature.mark_as_used(coupon)

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

        order_info = await self.order_feature.generate_order_info(order_number, order_items, subtotal, discount, shipping_cost, order_total)

        # Send the successful order email to customer and myself
        await self.email_feature.send_order_confirmation_email_to_customer(email, customer_info, order_info)
        await self.email_feature.send_email_to_me(customer_id, order_number, order_id)

        resp.media = {"order_number": order_number}
        resp.status = HTTP_OK
