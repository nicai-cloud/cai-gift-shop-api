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

    @route.get("/auto-complete", auth_exempt=True)
    async def auto_complete(self, req, resp):
        api_key = get('TOM_TOM_API_KEY')
        query = req.params.get("address")
        url = f"https://api.tomtom.com/search/2/search/suggest.json?key={api_key}&query={query}&countrySet=AU&typeahead=true&limit=5"

        ssl_context = ssl.create_default_context(cafile=certifi.where())

        async with ClientSession(connector=TCPConnector(ssl=ssl_context)) as session:
            try:
                response = await session.get(url=url)
                response.raise_for_status()
                if response.status == 200:
                    resp_json = await response.json()
                    print(f"resp_json: {resp_json}")
                    return resp_json
                    # return await response.json()
                else:
                    return {}
            except json.JSONDecodeError:
                print(
                    "Invalid JSON response from PM server calling telco/user/{suid}. If on local, make sure your VPN is on."
                )
                return {}

        
        response = requests.get(url)
        if response.status_code == 200:
            suggestions = response.json()['results']
            for suggestion in suggestions:
                print(suggestion['address']['freeformAddress'])

            resp.media = {"message": "Hello world!"}
            resp.status = falcon.HTTP_OK
        else:
            print("Error:", response.status_code, response.text)
