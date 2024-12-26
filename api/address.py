from aiohttp import ClientSession, TCPConnector
import falcon
import json
import ssl
import certifi
from urllib.parse import quote_plus

from api.base import RequestHandler, route
from features.address_feature import AddressFeature


class AddressRequestHandler(RequestHandler):
    def __init__(self):
        super().__init__()
        self.address_feature = AddressFeature()

    @route.post("/auto-complete/local", auth_exempt=True)
    async def auto_complete(self, req, resp):
        request_body = await req.get_media()
        if "search" not in request_body:
            raise falcon.HTTPInternalServerError(description="Missing search")
        
        query = request_body["search"]
        url = f"http://localhost:8080/addresses?q={quote_plus(query)}"

        print('url', url)

        ssl_context = ssl.create_default_context(cafile=certifi.where())

        async with ClientSession(connector=TCPConnector(ssl=ssl_context)) as session:
            try:
                response = await session.get(url=url)
                response.raise_for_status()
                addresses = []
                if response.status == 200:
                    suggestions = await response.json()
                    for suggestion in suggestions:
                        addresses.append(suggestion['sla'])

                    resp.media = {"addresses": addresses}
                    resp.status = falcon.HTTP_OK
                else:
                    resp.media = {}
            except json.JSONDecodeError:
                resp.media = {}

    @route.post("/auto-complete", auth_exempt=True)
    async def auto_complete_amazon(self, req, resp):
        request_body = await req.get_media()
        if "search" not in request_body:
            raise falcon.HTTPInternalServerError(description="Missing search")
        
        query = request_body["search"]
        suggestions = self.address_feature.get_address_suggestions(partial_text=query, max_results=10)
        resp.media = {"addresses": suggestions}
