from pprint import pprint

import requests

from config import sheety_headers, SHEETY_ENDPOINT, SHEETY_API_KEY
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

response = requests.get(url=f"{SHEETY_ENDPOINT}/{SHEETY_API_KEY}/copyOfFlightDeals/prices", headers=sheety_headers)
response.raise_for_status()
sheet_data = response.json()['prices']
# pprint(sheet_data)
for sheet in sheet_data:
    if sheet['iataCode'] == '':
        flight_search = FlightSearch(sheet['city'])
        sheet['iataCode'] = flight_search.search_iata_code()
        # update IATA codes in google sheets
        data_manager = DataManager(sheet['id'], sheet['iataCode'])
        data_manager.update_iata_code()

starting_point = input("which city would you like to start at? ")
search = FlightSearch(starting_point)


def find_lowest_price(data):
    min_price = data[0]['lowestPrice']
    for i in range(1, len(data)):
        min_price = min(min_price, data[i]['lowestPrice'])

    return min_price


lowest_price = find_lowest_price(sheet_data)
for sheet in sheet_data:
    # search for flights
    dest = sheet['iataCode']
    search_result = search.search_flights(dest)
    if search_result is not None:
        print(f"{search_result.destination_city}: ${search_result.price}")
    #  final step is to check if any of the flights found are cheaper than the Lowest Price listed in the Google
    #  Sheet. If so, then we should use the Twilio API to send an SMS with enough information to book the flight.
        if search_result.price < lowest_price:
            notification_manager = NotificationManager(search_result)
            notification_manager.send_sms()
