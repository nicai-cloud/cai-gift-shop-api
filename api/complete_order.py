from api.base import RequestHandler, route
from features.payment_method_feature import PaymentMethodFeature
from features.customer_feature import CustomerFeature
from features.order_feature import OrderFeature
from features.order_item_feature import OrderItemFeature
from infrastructure.work_management import WorkManager


class CompleteOrderRequestHandler(RequestHandler):
    def __init__(self, work_manager: WorkManager):
        super().__init__()
        self.customer_feature = CustomerFeature(work_manager)
        self.order_item_feature = OrderItemFeature(work_manager)
        self.order_feature = OrderFeature(work_manager)
        self.payment_method_feature = PaymentMethodFeature()

    @route.post("/", auth_exempt=True)
    async def complete_order(self, req, resp):
        request_body = await req.get_media()
        print('request_body', request_body)

        first_name = request_body["first_name"]
        last_name = request_body["last_name"]
        email = request_body["email"]
        mobile = request_body["mobile"]
        address = request_body["address"]
        payment_method_id = request_body["payment_method_id"]
        amount = 1000

        # Make the payment
        await self.payment_method_feature.create_payment_intent(payment_method_id, amount)

        # Create customer
        customer_id = await self.customer_feature.create_customer(first_name, last_name, email, mobile, address)
        print('!! created customer id: ', customer_id)

        # Create order item
        quantity = request_body["quantity"]
        preselection_id = request_body.get("preselection_id", None)
        bag_id = request_body.get("bag_id", None)
        item_ids = request_body.get("item_ids", None)
        order_item_id = await self.order_item_feature.create_order_item(quantity, preselection_id, bag_id, item_ids)
        print('!! created order item id: ', order_item_id)

        # Create an order against the customer
        await self.order_feature.create_order(customer_id=customer_id, order_item_id=order_item_id)
