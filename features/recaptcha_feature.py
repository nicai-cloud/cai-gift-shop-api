import logging
import requests
from utils.config import get

LOG = logging.getLogger(__name__)

RECAPTCHA_SECRET_KEY = get("RECAPTCHA_SECRET_KEY")


class RecaptchaFeature:
    def __init__(self):
        super().__init__()

    async def verify_captcha(self, token: str):
        url = "https://www.google.com/recaptcha/api/siteverify"
        payload = {
            "secret": RECAPTCHA_SECRET_KEY,
            "response": token
        }
        response = requests.post(url, data=payload)
        result = response.json()
        return result.get("success", False) and result.get("score", 0) > 0.5 and result.get('action') == 'complete_order'
