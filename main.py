from pprint import pprint

import requests

from config import sheety_headers, SHEETY_ENDPOINT, SHEETY_API_KEY
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

# update IATA codes in google prices sheets
response = requests.get(url=f"{SHEETY_ENDPOINT}/{SHEETY_API_KEY}/copyOfFlightDeals/prices", headers=sheety_headers)
response.raise_for_status()
sheet_data = response.json()['prices']
# pprint(sheet_data)
for sheet in sheet_data:
    if sheet['iataCode'] == '':
        flight_search = FlightSearch(sheet['city'])
        sheet['iataCode'] = flight_search.search_iata_code()
        data_manager = DataManager(sheet['id'], sheet['iataCode'])
        data_manager.update_iata_code()

# create new user in google users sheets
print("Welcome to Runyu's Flight Club")
print("We find the best flight deals and email you.")
existing_user = input("Are you an existing user? Please enter yes or no").lower()
if existing_user == "no":
    first_name = input("What is your first name?")
    last_name = input("What is your last name?")
    right_email = False
    while not right_email:
        email = input("What is your email?")
        verify_email = input("Type your email again")
        if email == verify_email:
            # input new row in google sheets
            new_user = {
                "user": {
                    "firstName": first_name,
                    "lastName": last_name,
                    "email": email
                }
            }
            response = requests.post(url=f"{SHEETY_ENDPOINT}/{SHEETY_API_KEY}/copyOfFlightDeals/users", json=new_user,
                                     headers=sheety_headers)
            response.raise_for_status()
            # print(response.text)
            print("You're in the club!")
            right_email = True
        else:
            print("Wrong email, please type again.")

starting_point = input("which city would you like to start at? ")
search = FlightSearch(starting_point)

for sheet in sheet_data:
    # search for flights
    dest = sheet['iataCode']
    search_result = search.search_flights(dest)
    if search_result is not None:
        print(f"{search_result.destination_city}: ${search_result.price}")
        #  final step is to check if any of the flights found are cheaper than the Lowest Price listed in the Google
        #  Sheet. If so, then we should use the Twilio API to send an SMS with enough information to book the flight.
        if search_result.price < sheet['lowestPrice']:
            # send sms
            notification_manager = NotificationManager(search_result)
            notification_manager.send_sms()
            # send email
            res = requests.get(url=f"{SHEETY_ENDPOINT}/{SHEETY_API_KEY}/copyOfFlightDeals/users", headers=sheety_headers)
            res.raise_for_status()
            user_data = res.json()['users']
            for usr_data in user_data:
                notification_manager.send_emails(usr_data)
