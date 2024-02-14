import requests
from bs4 import BeautifulSoup, NavigableString, Tag

import helpers.csv_helper as ch
import helpers.file_helper as fh
import helpers.http_helper as hh
import helpers.json_helper as jh
from constants import is_caching_enabled, searching_job_titles
from models.job_details import JobDetails

job_details_list_json_file_name = "tanqeeb_job_details_list.json"
job_list_json_file_name = "tanqeeb_job_list.json"

job_details_list_csv_file_name = "tanqeeb_job_details_list.csv"


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

    print("Fetched tanqeeb job count: 0", end="\r")

    job_list = []

    for job_title in job_titles:

        is_last_page = False
        page_number = 0

        generated_job_title_for_url = job_title.lower().replace(" ", "+")

        # region curl Converter
        # cookies = {
        #     "_ga": "GA1.1.772783286.1707209523",
        #     "IbJobView20077831": "20077831",
        #     "IbJobView20116497": "20116497",
        #     "IbJobView20070814": "20070814",
        #     "CAKEPHP": "332tajp6ver7bsce2pm57ve817",
        #     "PREF_LANG": "en",
        #     "_ga_HVWGXFNQQK": "GS1.1.1707846619.3.1.1707848943.0.0.0",
        # }

        # headers = {
        #     "authority": "saudi.tanqeeb.com",
        #     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        #     "accept-language": "en-US,en;q=0.9",
        #     "cache-control": "max-age=0",
        #     # 'cookie': '_ga=GA1.1.772783286.1707209523; IbJobView20077831=20077831; IbJobView20116497=20116497; IbJobView20070814=20070814; CAKEPHP=332tajp6ver7bsce2pm57ve817; PREF_LANG=en; _ga_HVWGXFNQQK=GS1.1.1707846619.3.1.1707848943.0.0.0',
        #     "referer": "https://saudi.tanqeeb.com/jobs/search?keywords=software+engineer&countries[]=54&page_no=2&order_by=most_recent&search_in=f&dictionary=1&change_lang=1",
        #     "sec-ch-ua": '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
        #     "sec-ch-ua-mobile": "?0",
        #     "sec-ch-ua-platform": '"Windows"',
        #     "sec-fetch-dest": "document",
        #     "sec-fetch-mode": "navigate",
        #     "sec-fetch-site": "same-origin",
        #     "sec-fetch-user": "?1",
        #     "upgrade-insecure-requests": "1",
        #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
        # }

        # response = requests.get(
        #     "https://saudi.tanqeeb.com/jobs/search?keywords=software+engineer&countries[]=54&page_no=1&order_by=most_recent&search_in=f&dictionary=1&",
        #     cookies=cookies,
        #     headers=headers,
        #     timeout=5,
        # )
        # endregion curl Converter

        while not is_last_page:

            page_number = page_number + 1

            curl_command = """
            curl 'https://saudi.tanqeeb.com/jobs/search?keywords={job_title}&country=54&state=0&page_no={page_number}&search_period=0&order_by=most_recent&search_in=f&lang=all' \
            -H 'authority: saudi.tanqeeb.com' \
            -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
            -H 'accept-language: en-US,en;q=0.9' \
            -H 'cookie: _ga=GA1.1.772783286.1707209523; IbJobView20077831=20077831; IbJobView20116497=20116497; IbJobView20070814=20070814; CAKEPHP=332tajp6ver7bsce2pm57ve817; PREF_LANG=en; _ga_HVWGXFNQQK=GS1.1.1707846619.3.1.1707851141.0.0.0' \
            -H 'referer: https://saudi.tanqeeb.com/en?change_lang=1' \
            -H 'sec-ch-ua: "Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"' \
            -H 'sec-ch-ua-mobile: ?0' \
            -H 'sec-ch-ua-platform: "Windows"' \
            -H 'sec-fetch-dest: document' \
            -H 'sec-fetch-mode: navigate' \
            -H 'sec-fetch-site: same-origin' \
            -H 'sec-fetch-user: ?1' \
            -H 'upgrade-insecure-requests: 1' \
            -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0' \
            --compressed
            """.replace(
                "{job_title}", generated_job_title_for_url
            ).replace(
                "{page_number}", f"{page_number}"
            )

            request_value = hh.curl_to_requests(curl_command)
            cookie_value = hh.request_to_cookies(request_value)
            base_url, query_params = hh.parse_query_params(curl_command)

            # query_params["page_no"] = page_number
            # query_params["keywords"] = generated_job_title_for_url
            # request_value.headers.pop("cookie")

            response = requests.request(
                method=request_value.method,
                url=request_value.url,
                headers=request_value.headers,
                # params=query_params,
                cookies=cookie_value,
                timeout=5,
            )

            page_soup = BeautifulSoup(response.text, "html.parser")

            next_page_button = page_soup.find(
                "ul", {"class": "pagination justify-content-center"}
            )

            # job_card_tag_list = page_soup.find_all(
            #     "div",
            #     "d-flex justify-content-between",
            # )

            job_card_tag_list = page_soup.find_all(
                "a",
                {
                    "class": "card-list-item card-list-item-hover px-3 px-lg-6 py-6 py-lg-4"
                },
            )

            for item in job_card_tag_list:
                job_card_tag: Tag | NavigableString | None = item

                job_title = job_card_tag.find(
                    "h2", {"class": "mb-2 hover-title fs-16 fs-18-lg"}
                ).text.strip()

                company_name = ""
                location = ""

                job_details = JobDetails(
                    job_title=job_title, location=location, company_name=company_name
                )

                job_list.append(job_details)
                print(f"Fetched tanqeeb job count: {len(job_list)}", end="\r")

            is_last_page = next_page_button.text.count("Next") == 0

    print(f"Fetched tanqeeb job count: {len(job_list)}")
    print("Fetched all tanqeeb jobs\n")
    return job_list
