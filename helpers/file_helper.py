import os


def read_file_as_string(file_path: str):
    """
    The function `read_file_as_string` reads the contents of a file as a string if the file exists, and
    returns `None` otherwise.
    
    :param file_path: The `file_path` parameter is a string that represents the path to the file that
    you want to read. It should include the file name and extension. For example, if the file is located
    in the current directory and its name is "example.txt", the `file_path` parameter would be "
    :type file_path: str
    :return: The function `read_file_as_string` returns the content of the file as a string if the file
    exists and can be read successfully. If the file does not exist or there is an error while reading
    the file, the function returns `None`.
    """
    # Check if the file exists in the current directory
    file_exists = os.path.isfile(file_path)

    if not file_exists:
        return None

    try:
        # Open the file in read mode
        with open(file_path, "r", encoding="utf8") as file:
            # Read the file as a string
            content = file.read()
        return content
    except Exception as ex:
        return None


def save_string_into_file(string: str, file_path: str):
    """
    The function `save_string_into_file` takes a string and a file path as input, and saves the string
    into a file at the specified path.
    
    :param string: The `string` parameter is a string that you want to save into a file. It can be any
    text or data that you want to write into the file
    :type string: str
    :param file_path: The file path is the location where you want to save the file. It can be an
    absolute path (e.g., "C:/Users/username/Documents/file.txt") or a relative path (e.g., "file.txt" if
    the file is in the same directory as your Python script)
    :type file_path: str
    """
    # Open a file in write mode
    with open(file_path, "w", encoding="utf8") as file:
        # Write the string to the file
        file.write(string)
