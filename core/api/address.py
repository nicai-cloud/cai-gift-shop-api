from aiohttp import ClientSession, TCPConnector
import falcon
import json
import ssl
import certifi
from utils.config import get

from core.api.base import RequestHandler, route


class AddressRequestHandler(RequestHandler):
    def __init__(self):
        super().__init__()

    @route.post("/auto-complete", auth_exempt=True)
    async def auto_complete(self, req, resp):
        api_key = get('TOM_TOM_API_KEY')
        
        request_body = await req.get_media()
        if "search" not in request_body:
            raise falcon.HTTPInternalServerError(description="Missing search")
        
        query = request_body["search"]
        url = f"https://api.tomtom.com/search/2/search/suggest.json?key={api_key}&query={query}&countrySet=AU&typeahead=true&limit=5"

        ssl_context = ssl.create_default_context(cafile=certifi.where())

        async with ClientSession(connector=TCPConnector(ssl=ssl_context)) as session:
            try:
                response = await session.get(url=url)
                response.raise_for_status()
                addresses = []
                if response.status == 200:
                    suggestions = (await response.json())['results']
                    for suggestion in suggestions:
                        addresses.append(suggestion['address']['freeformAddress'])

                    resp.media = {"addresses": addresses}
                    resp.status = falcon.HTTP_OK
                else:
                    resp.media = {}
            except json.JSONDecodeError:
                resp.media = {}
