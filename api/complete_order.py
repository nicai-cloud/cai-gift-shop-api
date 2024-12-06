from api.base import RequestHandler, route
from features.payment_method_feature import PaymentMethodFeature
from features.customer_feature import CustomerFeature
from infrastructure.work_management import WorkManager
from infrastructure.customer import CustomerRepo


class CompleteOrderRequestHandler(RequestHandler):
    def __init__(self, work_manager: WorkManager):
        super().__init__()
        customer_repo = work_manager.get(CustomerRepo)
        self.customer_feature = CustomerFeature(customer_repo)
        self.payment_method_feature = PaymentMethodFeature()

    @route.post("/", auth_exempt=True)
    async def complete_order(self, req, resp):
        request_body = await req.get_media()
        print('request_body', request_body)
        payment_method_id = request_body["payment_method_id"]
        amount = 1000

        # Make the payment
        await self.payment_method_feature.create_payment_intent(payment_method_id, amount)

        # Create customer record
        