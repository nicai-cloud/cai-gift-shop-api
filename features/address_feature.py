import aiohttp
from utils.config import get


class AddressFeature:
    def __init__(self):
        super().__init__()

    async def get_address_suggestions(self, partial_text: str) -> list[str]:
        async with aiohttp.ClientSession() as session:
            url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json'
            params = {
                'input': partial_text,
                'types': 'address',
                'components': 'country:au',
                'key': get("GOOGLE_MAPS_API_KEY")
            }

            async with session.get(url, params=params) as response:
                data = await response.json()
                if data.get('status') != 'OK':
                    print(f"Autocomplete Error: {data.get('status')}")
                    return []

                return [p['description'] for p in data['predictions']]
