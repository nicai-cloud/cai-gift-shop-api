from falcon import HTTP_OK

from api.base import RequestHandler, route


class HealthCheckRequestHandler(RequestHandler):
    def __init__(self):
        super().__init__()

    @route.get("/", auth_exempt=True)
    async def health_check(self, req, resp):
        resp.media = {"message": "Hello world!"}
        resp.status = HTTP_OK
