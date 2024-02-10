import time
from urllib.parse import parse_qs, urlparse

import convert_to_requests
import requests
from convert_to_requests import RequestData


def make_http_request(
    method: str,
    url: str,
    params=None,
    headers=None,
    cookies=None,
    files=None,
    timeout=10,
):
    while True:
        try:

            if cookies is None:
                return requests.request(
                    method,
                    url,
                    params=params,
                    headers=headers,
                    files=files,
                    timeout=timeout,
                )
            else:
                return requests.request(
                    method,
                    url,
                    params=params,
                    headers=headers,
                    cookies=cookies,
                    files=files,
                    timeout=timeout,
                )

        except Exception as ex:
            time.sleep(5)


def parse_query_params(url):
    """
    The function `parse_query_params` takes a URL as input and returns the base URL and the query
    parameters as a dictionary.

    :param url: The `url` parameter is a string that represents a URL with query parameters
    :return: The function `parse_query_params` returns two values: `base_url` and `query_params`.
    """

    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    base_url = f"{parsed_url.scheme}://{parsed_url.hostname}{parsed_url.path}"
    return base_url, query_params


def request_to_cookies(request: RequestData):
    cookie_string = request.headers["cookie"]
    # Split the string by ';' to separate individual cookies
    cookies = cookie_string.split("; ")

    # Initialize an empty dictionary to store key-value pairs
    cookie_dict = {}

    # Iterate over each cookie and split by '=' to separate key and value
    for cookie in cookies:
        key, value = cookie.split("=", 1)
        cookie_dict[key] = value

    return cookie_dict


def curl_to_requests(curl_command):
    """
    The function `curl_to_requests` converts a curl command into a requests library request object.

    :param curl_command: A string representing a curl command
    :return: a request object.
    """
    request = convert_to_requests.curl_to_requests(curl_command)

    return request
