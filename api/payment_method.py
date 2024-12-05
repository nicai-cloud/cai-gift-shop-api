import stripe
from api.base import RequestHandler, route
from utils.config import get

stripe.api_key = get("STRIPE_SECRET_KEY")


class PaymentMethodRequestHandler(RequestHandler):
    def __init__(self):
        super().__init__()

    @route.post("/", auth_exempt=True)
    async def create_payment_method(self, req, resp):
        try:
            # Create a PaymentMethod using a token
            payment_method = stripe.PaymentMethod.create(
                type="card",
                card={"token": 'tok_visa'}
            )
            resp.media = payment_method
        except stripe.error.CardError as e:
            # Handle declined card or 3D Secure required
            return {"error": str(e)}
        except Exception as e:
            # Handle other errors
            return {"error": str(e)}
