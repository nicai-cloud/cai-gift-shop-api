from falcon import HTTP_OK

from api.base import RequestHandler, route
from api.response_types import HealthcheckResponse


class HealthCheckRequestHandler(RequestHandler):
    def __init__(self):
        super().__init__()

    @route.get("/", auth_exempt=True)
    async def health_check(self, req, resp):
        resp.media = HealthcheckResponse(message="success")
        resp.status = HTTP_OK
