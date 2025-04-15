from falcon import HTTPInternalServerError

from api.base import RequestHandler, route
from features.address_feature import AddressFeature


class AddressRequestHandler(RequestHandler):
    def __init__(self):
        super().__init__()
        self.address_feature = AddressFeature()

    @route.post("/auto-complete", auth_exempt=True)
    async def auto_complete_amazon(self, req, resp):
        request_body = await req.get_media()
        if "search" not in request_body:
            raise HTTPInternalServerError(description="Missing search")
        
        query = request_body["search"]
        suggestions = await self.address_feature.get_address_suggestions(partial_text=query)
        resp.media = {"addresses": suggestions}
