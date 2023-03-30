from twilio.rest import Client

from config import TWILIO_SID, TWILIO_AUTH_TOKEN, FROM_NUMBER, TO_NUMBER
from flight_data import FlightData


class NotificationManager:

    def __init__(self, search_result: FlightData):
        self.search_result = search_result

    def send_sms(self):
        # send an SMS with enough information to book the flight
        price = self.search_result.price
        departure_city_name = self.search_result.origin_city
        departure_iata_code = self.search_result.origin_airport
        destination_city_name = self.search_result.destination_city
        destination_iata_code = self.search_result.destination_airport
        outbound_date = self.search_result.out_date
        inbound_date = self.search_result.return_date
        formatted_message = f"Low price alert! Only ${price} to fly from {departure_city_name}-{departure_iata_code} to " \
                            f"{destination_city_name}-{destination_iata_code}, from {outbound_date} to {inbound_date}."
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

        print("TWILIO SID is " + TWILIO_SID)
        print("TWILIO AUTH TOKEN is " + TWILIO_AUTH_TOKEN)
        print("FROM NUMBER is " + FROM_NUMBER)
        print("TO NUMBER is " + TO_NUMBER)
        message = client.messages.create(
            body=formatted_message,
            from_=FROM_NUMBER,
            to=TO_NUMBER
        )
        print(message.status)
