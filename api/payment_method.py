from api.base import RequestHandler, route
from features.payment_method_feature import PaymentMethodFeature


class PaymentMethodRequestHandler(RequestHandler):
    def __init__(self):
        super().__init__()
        self.payment_method_feature = PaymentMethodFeature()

    @route.post("/", auth_exempt=True)
    async def create_payment_method(self, req, resp):
        resp.media = await self.payment_method_feature.create_payment_method()
