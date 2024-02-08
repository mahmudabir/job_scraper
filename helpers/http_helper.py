from urllib.parse import parse_qs, urlparse

import convert_to_requests


def parse_query_params(url):
    """
    The function `parse_query_params` takes a URL as input and returns the base URL and the query
    parameters as a dictionary.

    :param url: The `url` parameter is a string that represents a URL with query parameters
    :return: The function `parse_query_params` returns two values: `base_url` and `query_params`.
    """

    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    base_url = f"{parsed_url.scheme}://{parsed_url.hostname}/{parsed_url.path}"
    return base_url, query_params


def curl_to_requests(curl_command):
    """
    The function `curl_to_requests` converts a curl command into a requests library request object.

    :param curl_command: A string representing a curl command
    :return: a request object.
    """
    request = convert_to_requests.curl_to_requests(curl_command)

    return request
