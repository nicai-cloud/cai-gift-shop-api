from api.base import RequestHandler, route
from features.payment_method_feature import PaymentMethodFeature
from features.customer_feature import CustomerFeature
from features.order_feature import OrderFeature
from infrastructure.work_management import WorkManager


class CompleteOrderRequestHandler(RequestHandler):
    def __init__(self, work_manager: WorkManager):
        super().__init__()
        self.customer_feature = CustomerFeature(work_manager)
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

        # Create an order against the customer
        await self.order_feature.create_order()
