import logging

import requests  # type: ignore


def url_request_handler(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-2xx response codes
        data = response.json()
        return data

    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise
    except requests.exceptions.JSONDecodeError as e:
        logging.error(f"Error decoding JSON response: {e}")
        raise
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred during the request: {e}")
        raise