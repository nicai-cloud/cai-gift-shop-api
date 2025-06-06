from falcon import HTTPBadRequest
import logging
import stripe
from decimal import Decimal
from utils.config import get

LOG = logging.getLogger(__name__)

stripe.api_key = get("STRIPE_SECRET_KEY")


class PaymentFeature:
    def __init__(self):
        super().__init__()

    async def create_payment_intent(self, amount_in_dollars: Decimal):
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=int(amount_in_dollars * 100),  # amount in cents
                currency="aud",
                payment_method_types=["card"],
                payment_method_options={
                    "card": {
                        "request_three_d_secure": "any"
                    }
                },
            )
            return payment_intent.client_secret
        except Exception as e:
            return {"error": str(e)}

    async def validate_payment_intent(self, payment_intent_id):
        if not payment_intent_id:
            raise HTTPBadRequest(
                title="Missing PaymentIntent ID",
                description="Missing PaymentIntent ID."
            )
        
        try:
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        except stripe.error.StripeError as e:
            raise HTTPBadRequest(
                title="Error retrieving PaymentIntent",
                description="Error retrieving PaymentIntent."
            )

        if payment_intent.status != 'succeeded':
            raise HTTPBadRequest(
                title="Payment not successful",
                description="Payment not successful."
            )

    async def confirm_payment_intent(self, payment_intent_id):
        stripe.PaymentIntent.confirm(
            payment_intent_id,
            payment_method="pm_card_visa",
            return_url="https://www.example.com",
        )
