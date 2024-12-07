from api.base import RequestHandler, route
from features.email_feature import EmailFeature


class EmailRequestHandler(RequestHandler):
    def __init__(self):
        super().__init__()
        self.email_feature = EmailFeature()


    @route.post("/send", auth_exempt=True)
    async def send_email(self, req, resp):
        request_body = await req.get_media()
        to_email = request_body["to_email"]
        order_id = request_body["order_id"]
        await self.email_feature.send_email(to_email, order_id)
