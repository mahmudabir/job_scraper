import re
from urllib.parse import parse_qs, urlparse

import convert_to_requests


def parse_query_params(url):
    """
    Parse query parameters from the given URL.

    Args:
    url (str): The URL to parse.

    Returns:
    dict: A dictionary containing the parsed query parameters.
    """
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    base_url = f"{parsed_url.scheme}://{parsed_url.hostname}/{parsed_url.path}"
    return base_url, query_params


def curl_to_requests(curl_command):
    request = convert_to_requests.curl_to_requests(curl_command)

    return request
