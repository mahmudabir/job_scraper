import re

from bs4 import BeautifulSoup, NavigableString, Tag

import helpers.csv_helper as ch
import helpers.file_helper as fh
import helpers.http_helper as hh
import helpers.json_helper as jh
from constants import is_caching_enabled, searching_job_titles
from models.job_details import JobDetails

job_details_list_json_file_name = "bayt_job_details_list.json"
job_list_json_file_name = "bayt_job_list.json"

job_details_list_csv_file_name = "bayt_job_details_list.csv"


def start_scraping():

    job_list: list[JobDetails] = get_all_job_paged_list()

    ch.list_to_csv_file(job_list, job_details_list_csv_file_name)


def generate_job_details_list_for_csv_file(job_paged_list, job_details_response_list):
    job_details_list_for_csv: list[JobDetails] = []

    for job_details_response_item in job_details_response_list:

        job_details_item = job_details_response_item["jobDetailResponse"]
        job_page_item = list(
            filter(
                lambda job: job["id"] == job_details_item["id"],
                job_paged_list,
            )
        )[0]

        job_detail = JobDetails(
            job_title=job_details_item["title"],
            location=f"{job_page_item['locations']} - Saudi Arabia",
            company_name=job_details_item["company"]["name"],
            # website=job_details_item["title"],
            # email=job_details_item["title"],
            # phone=job_details_item["title"],
        )
        job_details_list_for_csv.append(job_detail)

    return job_details_list_for_csv


def get_all_job_paged_list():
    job_list = []
    job_list_string = fh.read_file_as_string(job_list_json_file_name)

    if (
        not is_caching_enabled
        or job_list_string is None
        or job_list_string == ""
        or job_list_string == "{}"
        or job_list_string == "[]"
    ):
        job_list = scrap_job_list_from_website()
        fh.save_string_into_file(
            jh.data_to_json_string(job_list), job_list_json_file_name
        )
    else:
        job_list = jh.json_string_to_data(job_list_string)

    return job_list


def scrap_job_list_from_website():
    job_list = []
    job_list = job_list.__add__(fetch_jobs_by_job_title(searching_job_titles))

    return job_list


def fetch_jobs_by_job_title(job_titles: list[str]):

    print("Fetched bayt job count: 0", end="\r")

    job_list = []

    for job_title in job_titles:

        is_last_page = False
        page_number = 0

        base_url, query_params = hh.parse_query_params(
            f"https://www.bayt.com/en/saudi-arabia/jobs/{generate_job_path_parameter(job_title)}-jobs/?page=1"
        )

        while not is_last_page:

            page_number = page_number + 1
            query_params["page"] = page_number

            response = hh.make_http_request(
                method="GET", url=base_url, params=query_params
            )

            page_soup = BeautifulSoup(response.text, "html.parser")

            next_page_button = page_soup.find("li", {"class": "pagination-next"})

            # li, has-pointer-d
            job_card_tag_list = page_soup.find_all("li", "has-pointer-d")

            for item in job_card_tag_list:
                job_card_tag: Tag | NavigableString | None = item

                job_title = job_card_tag.find("h2", "jb-title m0 t-large").text.strip()
                company_name = job_card_tag.find("b", "jb-company").text.strip()
                location = job_card_tag.find(
                    "span", "jb-loc t-mute t-nowrap"
                ).text.strip()

                job_details = JobDetails(
                    job_title=job_title, location=location, company_name=company_name
                )

                job_list.append(job_details)
                print(f"Fetched bayt job count: {len(job_list)}", end="\r")

            is_last_page = next_page_button.get("class").count("u-none") > 0

    return job_list


def generate_job_path_parameter(job_title, job_id=None):
    path_param = re.sub(r"[^a-zA-Z0-9]+", "-", job_title).lower().strip("-")

    if job_id is not None:
        path_param = path_param.__add__(f"-{job_id}")

    return path_param
