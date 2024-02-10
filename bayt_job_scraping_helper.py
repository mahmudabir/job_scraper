import re

from convert_to_requests import RequestData

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

    job_list = get_all_job_paged_list()
    # job_details_list = get_all_job_details_list(job_list)

    # job_details_list_for_csv = generate_job_details_list_for_csv_file(
    #     job_list, job_details_list
    # )

    # ch.list_to_csv_file(job_details_list_for_csv, job_details_list_csv_file_name)


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


def get_all_job_details_list(job_list):
    job_details_list = []
    job_details_list_string = fh.read_file_as_string(job_details_list_json_file_name)

    if (
        not is_caching_enabled
        or job_details_list_string is None
        or job_details_list_string == ""
        or job_details_list_string == "{}"
        or job_details_list_string == "[]"
    ):
        job_details_list = scrap_all_job_details_from_website(job_list)
        fh.save_string_into_file(
            jh.data_to_json_string(job_details_list), job_details_list_json_file_name
        )
    else:
        job_details_list = jh.json_string_to_data(job_details_list_string)

    return job_details_list


def scrap_job_list_from_website():
    job_list = []

    for job_title in searching_job_titles:
        job_list = job_list.__add__(fetch_jobs_by_job_title(job_title))

    return job_list


def fetch_jobs_by_job_title(job_title: str):

    job_title_as_path_param = generate_job_path_parameter(job_title)

    is_last_page = False
    page_number = 0

    job_list = []

    curl_command = """
        curl 'https://www.bayt.com/en/saudi-arabia/jobs/{job_title}-jobs/?page=1' \
        -H 'authority: www.bayt.com' \
        -H 'accept: */*' \
        -H 'accept-language: en-US,en;q=0.9' \
        -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary9IBfJw0x2428o2XE' \
        -H 'cookie: brID=3826975085611352771409; cookieyes-consent=consentid:S2k4RFFzdHlnUEoxSWlCNUFEc05Jb0dWaHBaNnY1NTk,consent:yes,action:no,necessary:yes,functional:yes,analytics:yes,performance:yes,advertisement:yes; _ga=GA1.1.389913315.1707209511; __gsas=ID=41571183dd68857c:T=1707209581:RT=1707209581:S=ALNI_MZc0nqSK3NY7ayfwdyGvMgfYfVuVg; MSESID0=3828650276480934284453%2C0%2C0%2C0%2C48GNT9%2C0%2C5%2C630914585341f44347679dc65c1522b8; BSESINFO0=50%2CCGDOQ0%2C%2C; ISLOGGED0=0; SSD0=PCAO2llcNV6fJ0MG0eLZVQ76Te7dLYEvmy%2BFBYx3Jbl00cskHMS2pF4I8qQeRa3Z%40%40%401c31a8609029cd70; user-prefs=locale%20xx%20lang%20en%20geo%20bd; _clck=15f0ewu%7C2%7Cfj3%7C0%7C1497; aff_data={%22qs%22:%22%22%2C%22ref%22:%22https://www.bayt.com/%22}; g_state={"i_p":1707981844292,"i_l":3}; JB_SRCH_TKN=%2Bp74ax5jK44%3D1707377056; _uetsid=35fbd8f0c65511eeb9e88169b8962376; _uetvid=35fc88d0c65511ee9f6eb97066c9dc83; userSearchKeyword=software%20engineer%2Csoftware%20developer; NaviPageUrl=https://www.bayt.com/en/saudi-arabia/jobs/net-software-engineer-net-8-c-digital-downloads-saudi-arabia-4901022/; __gads=ID=b3e52d05f952ce47:T=1707209592:RT=1707384769:S=ALNI_MYkr0jGVettgiEbEqZux6SZDIVKow; __gpi=UID=00000cfa66bbb60c:T=1707209592:RT=1707384769:S=ALNI_MZO6Vj4jVeqX7m5pLPjgtZYeEnTcg; __eoi=ID=2b27901c35bde8bf:T=1707209592:RT=1707384769:S=AA-AfjYMri6wBpQNZpRp06P5Yiu8; rs=t=software%2520developer&con=saudi-arabia:t=software%2520engineer&con=saudi-arabia:t=software%2520engineer%2520software%2520developer&con=saudi-arabia:t=software%2520engineer&con=international:t=software%2520developer&con=international; _clsk=1ckt7xw%7C1707388431010%7C14%7C1%7Co.clarity.ms%2Fcollect; _ga_1NKPLGNKKD=GS1.1.1707387818.6.1.1707388435.50.0.0' \
        -H 'origin: https://www.bayt.com' \
        -H 'referer: https://www.bayt.com/en/saudi-arabia/jobs/{job_title}-jobs/?page=1' \
        -H 'sec-ch-ua: "Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"' \
        -H 'sec-ch-ua-mobile: ?0' \
        -H 'sec-ch-ua-platform: "Windows"' \
        -H 'sec-fetch-dest: empty' \
        -H 'sec-fetch-mode: cors' \
        -H 'sec-fetch-site: same-origin' \
        -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0' \
        -H 'x-requested-with: XMLHttpRequest' \
        --data-raw $'------WebKitFormBoundary9IBfJw0x2428o2XE\r\nContent-Disposition: form-data; name="listOnly"\r\n\r\ntrue\r\n------WebKitFormBoundary9IBfJw0x2428o2XE--\r\n' \
        --compressed
    """.replace(
        "{job_title}", job_title_as_path_param
    )

    http_request: RequestData = hh.curl_to_requests(curl_command)
    form_data = {"listOnly": True}

    # http_request.headers.pop("cookie")
    # cookies = hh.request_to_cookies(http_request)

    base_url, query_params = hh.parse_query_params(http_request.url)

    while not is_last_page:

        page_number = page_number + 1
        query_params["page"] = page_number

        response = hh.make_http_request(
            method=http_request.method,
            url=base_url,
            params=query_params,
            headers=http_request.headers,
            files=form_data,
            timeout=10,
        )

        if response.status_code == 401:
            is_last_page = True
            return job_list

        result = response.json()
        job_posts_dict: dict = result["data"]["jobPosts"]

        temp_job_list = [job_posts_dict[key] for key in job_posts_dict.keys()]

        job_list = job_list.__add__(temp_job_list)

        # fh.save_string_into_file(response.text, f"{page_number} - {job_title}.json")

        is_last_page = job_posts_dict.keys().__len__() == 0

    return job_list


def scrap_all_job_details_from_website(job_list):

    print(f"Total job count: {len(job_list)}")

    job_details_list = []

    for job in job_list:
        job_details_list.append(
            scrap_job_details(job.get("jb_title"), job.get("jb_id"))
        )
        print(f"Fetched job count: {len(job_details_list)}", end="\r")

    print(f"Fetched job count: {len(job_details_list)}")
    return job_details_list


def scrap_job_details(job_title, job_id):

    path_param_value = generate_job_path_parameter(job_title, job_id)

    response = hh.make_http_request(
        "GET",
        f"https://www.bayt.com/en/saudi-arabia/jobs/{path_param_value}/",
        timeout=5,
    )

    response_text = response.text

    json_string = (
        response_text.split("<title>")[0]
        .split("<script>")[1]
        .split("</script>")[0]
        .split("B8v=")[1]
        .replace(";", "")
    )

    json_details_obj = jh.json_string_to_data(json_string)
    return json_details_obj


def generate_job_path_parameter(job_title, job_id=None):
    path_param = re.sub(r"[^a-zA-Z0-9]+", "-", job_title).lower().strip("-")

    if job_id is not None:
        path_param = path_param.__add__(f"-{job_id}")

    return path_param
