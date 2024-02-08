import csv


def list_to_csv_file(
    data_list: list, csv_file_path: str, header_names: list[str] = None
):
    """
    The function `list_to_csv_file` takes a list of dictionaries or objects, along with an optional list
    of header names, and writes the data to a CSV file.

    :param data_list: The `data_list` parameter is a list of data that you want to write to a CSV file.
    Each element in the list can be either a dictionary or an object. If the elements are objects, they
    will be converted to dictionaries using the `vars()` function
    :type data_list: list
    :param csv_file_path: The `csv_file_path` parameter is a string that represents the file path where
    the CSV file will be created or overwritten. It should include the file name and the file extension
    ".csv". For example, "data.csv" or "C:/path/to/data.csv"
    :type csv_file_path: str
    :param header_names: The `header_names` parameter is a list of strings that represents the column
    names or headers for the CSV file. If this parameter is not provided, the function will try to infer
    the column names from the data list
    :type header_names: list[str]
    """

    if data_list is not None or data_list.__len__() > 0:

        data_list_type = type(data_list[0])

        if data_list_type is not dict:
            data_dict_list = list(map(vars, data_list))
            try:
                header_names: list[str] = header_names or list(
                    data_list[0].__dict__.keys()
                )
            except Exception as e:
                header_names: list[str] = header_names or get_all_keys(data_dict_list)
        else:
            data_dict_list = data_list
            header_names: list[str] = header_names or (get_all_keys(data_dict_list))

        # Write the list of Person objects to the CSV file
        with open(csv_file_path, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=header_names)

            # Write header
            writer.writeheader()

            # Write rows
            # writer.writerows(data_dict_list)

            for data in data_dict_list:
                writer.writerow(data)
    else:
        print("No data to write to CSV file.")


def get_all_keys(data_list: list):
    """
    The function `get_all_keys` takes a list of dictionaries as input and returns a list of all unique
    keys present in the dictionaries.

    :param data_list: A list of dictionaries where each dictionary represents a data entry
    :type data_list: list
    :return: a list of all the unique keys from the dictionaries in the input list.
    """
    # Initialize an empty set to collect keys
    all_keys = set()

    # Iterate over each dictionary in the list
    for dictionary in data_list:
        # Update the set of keys with the keys from the current dictionary
        all_keys.update(dictionary.keys())

    # Convert the set of keys to a list
    all_keys_list = list(all_keys)

    return all_keys_list


def csv_file_to_list(file_path: str):
    """
    The function `csv_file_to_list` takes a file path as input, reads a CSV file at that path, and
    returns a list of dictionaries where each dictionary represents a row in the CSV file.

    :param file_path: The file path is a string that represents the location of the CSV file that you
    want to convert to a list
    :type file_path: str
    :return: a list of dictionaries. Each dictionary represents a row in the CSV file, with the keys
    being the column names and the values being the corresponding values in that row.
    """

    with open(file_path, "r", encoding="utf8") as read_obj:
        # Return a reader object which will
        # iterate over lines in the given csvfile
        csv_reader = csv.reader(read_obj)

        # convert string to list
        list_of_rows = list(csv_reader)

        keys = list_of_rows[0]

        # Initialize an empty list to store dictionaries
        result = []

        # Iterate over the remaining lists and create dictionaries
        for row in list_of_rows[1:]:
            # Create a dictionary by zipping keys and values
            person_dict = dict(zip(keys, row))
            result.append(person_dict)

        return result
