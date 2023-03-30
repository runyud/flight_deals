from twilio.rest import Client

from config import TWILIO_SID, TWILIO_AUTH_TOKEN, FROM_NUMBER, TO_NUMBER, MY_EMAIL, MY_PASSWORD
from flight_data import FlightData
import smtplib
from smtplib import SMTPResponseException


class NotificationManager:

    def __init__(self, search_result: FlightData):
        self.formatted_msg = None
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
        self.formatted_msg = formatted_message
        if self.search_result.stop_overs > 0:
            formatted_message += f"\nFlight has {self.search_result.stop_overs} stop over, via {self.search_result.via_city}."
            print(formatted_message)

        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

        message = client.messages.create(
            body=formatted_message,
            from_=FROM_NUMBER,
            to=TO_NUMBER
        )
        print(message.status)

    def send_emails(self, user_data):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            # format the email
            formatted_email = self.formatted_msg.encode('ascii', 'ignore').decode('ascii')
            if self.search_result.deep_link is not None:
                formatted_email += f"\n{self.search_result.deep_link}"
            try:
                connection.sendmail(from_addr=MY_EMAIL, to_addrs=user_data['email'], msg=formatted_email)
            except SMTPResponseException as e:
                error_code = e.smtp_code
                error_message = e.smtp_error
                print(f"{error_code} : {error_message}")
