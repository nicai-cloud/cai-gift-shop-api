import logging
import stripe
from utils.config import get

LOG = logging.getLogger(__name__)

stripe.api_key = get("STRIPE_SECRET_KEY")


class PaymentMethodFeature:
    def __init__(self):
        pass
    
    async def create_payment_intent(self, payment_method_id, amount):
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
                return payment_intent["id"]
            else:
                print(f"Payment not successful: {payment_intent['status']}")
                return ""
        except stripe.error.CardError as e:
            # Handle declined card or 3D Secure required
            return {"error": str(e)}
        except Exception as e:
            # Handle other errors
            return {"error": str(e)}
        
    async def create_payment_method(self):
        try:
            # Create a PaymentMethod using a token
            payment_method = stripe.PaymentMethod.create(
                type="card",
                card={"token": 'tok_visa'}
            )
            return payment_method
        except stripe.error.CardError as e:
            # Handle declined card or 3D Secure required
            return {"error": str(e)}
        except Exception as e:
            # Handle other errors
            return {"error": str(e)}
