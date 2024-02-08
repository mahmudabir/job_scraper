import json


def json_string_to_data(json_string: str):
    """
    The function `json_string_to_data` takes a JSON string as input and returns the corresponding Python
    data structure.
    
    :param json_string: A string containing JSON data
    :type json_string: str
    :return: the data converted from the JSON string.
    """
    data = json.loads(json_string)
    return data


def data_to_json_string(data):
    """
    The function `data_to_json_string` converts data to a JSON string with specified formatting options.
    
    :param data: The `data` parameter is the data that you want to convert to a JSON string. It can be
    any valid Python data structure such as a dictionary, list, or object
    :return: a JSON string representation of the input data.
    """
    ensure_ascii_value = False
    indent_value = 4
    data = json.dumps(
        data,
        default=lambda x: x.__dict__,
        ensure_ascii=ensure_ascii_value,
        indent=indent_value,
    )
    return data
