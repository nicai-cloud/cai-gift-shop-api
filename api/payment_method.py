from api.base import RequestHandler, route
from features.payment_method import PaymentMethod


class PaymentMethodRequestHandler(RequestHandler):
    def __init__(self):
        super().__init__()
        self.payment_method = PaymentMethod()

    @route.post("/", auth_exempt=True)
    async def create_payment_method(self, req, resp):
        resp.media = await self.payment_method.create_payment_method()
