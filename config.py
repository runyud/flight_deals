import os

# SHEETY API CONFIGS
SHEETY_API_KEY = os.environ.get("SHEETY_KEY")
SHEETY_ENDPOINT = os.environ.get("SHEETY_ENDPOINT")
SHEETY_BEARER_TOKEN = os.environ.get("SHEETY_BEARER_TOKEN")

sheety_headers = {
    "Authorization": f"Bearer {SHEETY_BEARER_TOKEN}"
}


# KIWI API CONFIGS
KIWI_API_KEY = os.environ.get("KIWI_KEY")
KIWI_QUERY_ENDPOINT = os.environ.get("KIWI_QUERY_ENDPOINT")
KIWI_SEARCH_ENDPOINT = os.environ.get("KIWI_SEARCH_ENDPOINT")

kiwi_header = {
    "apikey": KIWI_API_KEY
}

# TWILIO API CONFIGS
TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_API_KEY = os.environ.get("TWILIO_API_KEY")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

# phone numbers
FROM_NUMBER = os.environ.get("FROM_NUMBER")
TO_NUMBER = os.environ.get("TO_NUMBER")

# Email configs
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")



