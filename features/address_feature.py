import boto3

# Initialize the Location Service client
client = boto3.client('location', region_name='ap-southeast-2')  # Australia region

PLACE_INDEX_NAME = "AustraliaAddressIndex"

class AddressFeature:
    def __init__(self):
        super().__init__()

    def get_address_suggestions(self, partial_text, max_results=5, country_filter=["AUS"]):
        """
        Fetches address autocomplete suggestions using Amazon Location Service.
        
        :param partial_text: The text input for address search.
        :param max_results: The maximum number of suggestions to return.
        :param country_filter: List of country codes to filter results (default: Australia ["AUS"]).
        :return: List of suggestions with details.
        """
        try:
            response = client.search_place_index_for_suggestions(
                IndexName=PLACE_INDEX_NAME,
                Text=partial_text,
                MaxResults=max_results,
                FilterCountries=country_filter
            )
            results = response.get("Results", [])
            suggestions = [result["Text"] for result in results if "AddressType" in result["Categories"]]
            return suggestions
        except Exception as e:
            print(f"Error: {e}")
            return []
