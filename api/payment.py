from falcon import HTTP_OK, HTTPBadRequest

from api.base import RequestHandler, route
from api.request_types import PaymentIntentRequest
from api.response_types import PaymentIntentResponse
from features.payment_feature import PaymentFeature
from features.order_feature import OrderFeature
from infrastructure.work_management import WorkManager

import marshmallow


class PaymentRequestHandler(RequestHandler):
    def __init__(self, work_manager: WorkManager):
        super().__init__()
        self.payment_feature = PaymentFeature()
        self.order_feature = OrderFeature(work_manager)

    @route.post("/payment-intent", auth_exempt=True)
    async def create_payment_intent(self, req, resp):
        raw_request_body = await req.get_media()
        try:
            request_body = PaymentIntentRequest.Schema().load(raw_request_body)
        except marshmallow.exceptions.ValidationError as e:
            raise HTTPBadRequest(title="Invalid request payload", description=str(e))
        
        order_items = request_body.order_items
        fulfillment_method = request_body.fulfillment_method

        subtotal, subtotal_after_discount = await self.order_feature.calculate_subtotal(order_items=order_items)
        shipping_cost = await self.order_feature.calculate_shipping_cost(fulfillment_method, subtotal)
        order_total = round(subtotal_after_discount + shipping_cost, 2)
    
        client_secret = await self.payment_feature.create_payment_intent(order_total)
        resp.media = PaymentIntentResponse(client_secret=client_secret)
        resp.status = HTTP_OK

    @route.post("/confirm-payment-intent", auth_exempt=True)
    async def confirm_payment_intent(self, req, resp):
        raw_request_body = await req.get_media()
        payment_intent_id = raw_request_body["payment_intent_id"]
        await self.payment_feature.confirm_payment_intent(payment_intent_id)
