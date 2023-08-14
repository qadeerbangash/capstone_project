from decouple import config
from utils import url_request_handler

base_url = config("BASE_URL")


def get_rating():
    url = f"{base_url}/rating"
    return url_request_handler(url)


def get_appointment():
    url = f"{base_url}/appointment"
    return url_request_handler(url)


def get_patient_councillor():
    url = f"{base_url}/patient_councillor"
    return url_request_handler(url)


def get_councillor():
    url = f"{base_url}/councillor"
    return url_request_handler(url)
    