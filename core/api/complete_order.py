import stripe
from core.api.base import RequestHandler, route
from utils.config import get

stripe.api_key = get("STRIPE_SECRET_KEY")


class CompleteOrderRequestHandler(RequestHandler):
    def __init__(self):
        super().__init__()

    @route.post("/", auth_exempt=True)
    async def complete_order(self, req, resp):
        request_body = await req.get_media()
        print('request_body', request_body)
        payment_method_id = request_body["payment_method_id"]
        amount = 1000

        try:
            # Create and confirm a PaymentIntent
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,  # Amount in the smallest currency unit, e.g., cents
                currency="aud",
                payment_method=payment_method_id,
                payment_method_types=["card"],
                confirm=True,  # Confirm immediately
            )
            if payment_intent["status"] == "succeeded":
                print(f"Payment succeeded: {payment_intent['id']}")
                return True, payment_intent["id"]
            else:
                print(f"Payment not successful: {payment_intent['status']}")
                return False, ""
        except stripe.error.CardError as e:
            # Handle declined card or 3D Secure required
            return {"error": str(e)}
        except Exception as e:
            # Handle other errors
            return {"error": str(e)}
