from datetime import datetime, timedelta
from pprint import pprint

import requests

from config import KIWI_QUERY_ENDPOINT, KIWI_SEARCH_ENDPOINT, kiwi_header
from flight_data import FlightData


class FlightSearch:

    def __init__(self, city_name):
        self.city_name = city_name

    def search_iata_code(self):
        # search iata code for the city name
        iata_query_params = {
            "term": self.city_name,
            "locale": "en-US",
            "location_types": "city",
            "limit": 1,
            "active_only": "true"
        }

        response = requests.get(url=KIWI_QUERY_ENDPOINT, params=iata_query_params, headers=kiwi_header)
        response.raise_for_status()
        iata_code = response.json()['locations'][0]['code']
        return iata_code

    def search_flights(self, destination) -> FlightData:
        # search for direct flights and round trips between source and destination within 6 months
        today = datetime.now()
        num_days = 180
        six_months = today + timedelta(days=num_days)
        start_date = today.strftime("%d/%m/%Y")
        end_date = six_months.strftime("%d/%m/%Y")
        # print("start date is " + start_date)
        # print("end date is " + end_date)

        flight_search_params = {
            "fly_from": self.city_name,
            "fly_to": destination,
            "date_from": start_date,
            "date_to": end_date,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "USD"
        }

        response = requests.get(url=KIWI_SEARCH_ENDPOINT, params=flight_search_params, headers=kiwi_header)
        response.raise_for_status()

        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {destination}.")
            return None

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )
        return flight_data
