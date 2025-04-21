import aiohttp
from utils.config import get
from api.types import AddressSuggestions


class AddressFeature:
    def __init__(self):
        super().__init__()

    async def get_address_suggestions(self, partial_text: str) -> AddressSuggestions:
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

                return AddressSuggestions(
                    addresses=[p['description'] for p in data['predictions']]
                )
