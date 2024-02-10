from bs4 import BeautifulSoup, NavigableString, ResultSet, Tag


def find_all_by_class_name(soup: BeautifulSoup, name=None, class_value=None):
    if class_value is None:
        class_value = ""
    return soup.find_all(name, {"class": class_value})


def find_one_by_class_names_from_soup(
    soup: BeautifulSoup, name: str = None, class_value: str = None
):
    if class_value is None:
        class_value = ""
    return soup.find(name, {"class": class_value})


def find_all_by_tag_name(
    result_set: ResultSet, name=None
) -> list[Tag | NavigableString | None]:
    tag_list: list[Tag | NavigableString | None] = [
        item.find(name) for item in result_set
    ]
    return tag_list


def find_one_by_class_name_from_tag(tag: Tag, class_name: str) -> Tag | None:
    result_tag = tag.select_one(f".{class_name}")
    return result_tag


def get_value_of_attributes(
    tag_list: list[Tag | NavigableString | None], attribute_name=None
):
    values: list[dict] = [
        {"tag": tag, "value": tag.get(key=attribute_name)} for tag in tag_list
    ]
    return values


def parse_html_content_as_string(content_str: str, features: str = "html.parser"):
    """
    The function `parse_html_content_as_string` takes a string containing HTML content and returns a
    BeautifulSoup object that can be used to parse and manipulate the HTML.

    :param content_str: The content_str parameter is a string that represents the HTML content that you
    want to parse. It can be any valid HTML content
    :type content_str: str
    :param features: The `features` parameter is used to specify the parser to be used by BeautifulSoup
    for parsing the HTML content. It can take different values depending on the parser library being
    used, defaults to html.parser
    :type features: str (optional)
    :return: a BeautifulSoup object.
    """
    return BeautifulSoup(content_str, features)
