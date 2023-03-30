import requests
from config import sheety_headers, SHEETY_ENDPOINT, SHEETY_API_KEY


class DataManager:

    def __init__(self, id, iata_code):
        self.row_id = id
        self.iata_code = iata_code

    def update_iata_code(self):
        # update google sheet with the IATA codes
        iata_code = {
            "price": {
                "iataCode": self.iata_code
            }
        }
        response = requests.put(url=f"{SHEETY_ENDPOINT}/{SHEETY_API_KEY}/copyOfFlightDeals/prices/{self.row_id}",
                                json=iata_code, headers=sheety_headers)
        response.raise_for_status()

