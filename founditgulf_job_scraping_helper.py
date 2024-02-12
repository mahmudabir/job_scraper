import helpers.csv_helper as ch
import helpers.file_helper as fh
import helpers.http_helper as hh
import helpers.json_helper as jh
from constants import is_caching_enabled, searching_job_titles
from models.job_details import JobDetails

job_details_list_json_file_name = "founditgulf_job_details_list.json"
job_list_json_file_name = "founditgulf_job_list.json"

job_details_list_csv_file_name = "founditgulf_job_details_list.csv"


def start_scraping():

    job_list = get_all_job_paged_list()
    job_details_list = get_all_job_details_list(job_list)

    job_details_list_for_csv = generate_job_details_list_for_csv_file(
        job_list, job_details_list
    )

    ch.list_to_csv_file(job_details_list_for_csv, job_details_list_csv_file_name)


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
        print("Fetched all founditgulf jobs\n")
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

    return [job for job in job_list if job.get("type") is None]


def fetch_jobs_by_job_title(job_title: str):

    last_page_number = 1
    page_number = 0

    # job_title_base = job_title
    # job_title = job_title.lower().replace(" ", "+")

    job_list = []

    curl_command = """
    curl 'https://www.founditgulf.com/middleware/jobsearch?start=15&sort=1&limit=15&query=Software%20Engineer&locations=Saudi%20Arabia&queryDerived=true' \
    -H 'authority: www.founditgulf.com' \
    -H 'accept: application/json, text/plain, */*' \
    -H 'accept-language: en-US,en;q=0.9' \
    -H 'cookie: _gcl_au=1.1.83993725.1707209517; G_ENABLED_IDPS=google; WZRK_G=0154b99c518a432a8cb4d3d6542bcfbe; _fbp=fb.1.1707209518057.1578193184; ajs_anonymous_id=%2218d7d9ded6b752-0ad7e09f4b1418-4c657b58-157872-18d7d9ded6cd5b%22; NHP=true; MSUID=5d4b0fc9-5b6d-4832-81aa-42c079e89859; uuidAB=f8602a65-9651-451f-8af9-cbd0d28a32df; _ga=GA1.1.1275091489.1707209518; _ga_P9R1Y92J7R=GS1.2.1707224481.2.1.1707224492.49.0.0; _clck=zg7d0k%7C2%7Cfj3%7C0%7C1497; __gads=ID=fa9bcd912bc33673:T=1707222553:RT=1707374896:S=ALNI_MbClSQyISRduZKHH_6z834hOVfMMg; __gpi=UID=00000cfa86d57d60:T=1707222553:RT=1707374896:S=ALNI_Ma2iMvTUrMPxoZylW0V1HrGnOtwwg; __eoi=ID=dc01cbf2c7076e26:T=1707222553:RT=1707374896:S=AA-AfjY0ahpHv2j5J8hIzyYBxpIx; WZRK_S_6K9-ZK8-ZZ6Z=%7B%22p%22%3A4%2C%22s%22%3A1707374895%2C%22t%22%3A1707374911%7D; _uetsid=fc45c010c4cc11ee8ca2974b877b220b; _uetvid=fc45d430c4cc11ee9b8f9f2e4b390d47; _clsk=1305qsm%7C1707374913391%7C8%7C1%7Co.clarity.ms%2Fcollect; FCNEC=%5B%5B%22AKsRol8_ztHhFGPwc4UsTd47RxlZDU-rpRAU9uo8hkKMyrupPVnDMi7lEbdIncgt6JPvo4AjxJ-PLViZzb0GyEXAlz0lYht0OR6m51Dc_TOaJ9LyaZICTklUgl4QPh83XBNYHSF5CqA5nqSungS0eWM-TbnC_SCixQ%3D%3D%22%5D%5D; _ga_B3CBFFVVNQ=GS1.1.1707374893.11.1.1707374923.30.0.0' \
    -H 'referer: https://www.founditgulf.com/srp/results?start=0&sort=1&limit=15&query=Software%20Engineer&locations=Saudi%20Arabia&queryDerived=true' \
    -H 'sec-ch-ua: "Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"' \
    -H 'sec-ch-ua-mobile: ?0' \
    -H 'sec-ch-ua-platform: "Windows"' \
    -H 'sec-fetch-dest: empty' \
    -H 'sec-fetch-mode: cors' \
    -H 'sec-fetch-site: same-origin' \
    -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0' \
    -H 'x-language-code: EN' \
    -H 'x-source-country: SA' \
    -H 'x-source-site-context: monstergulf' \
    --compressed
    """

    http_request = hh.curl_to_requests(curl_command)

    base_url, query_params = hh.parse_query_params(http_request.url)

    while page_number <= last_page_number:

        query_params["start"] = page_number * 15
        query_params["query"] = job_title
        # params["queryEntity"] = params["queryEntity"].replace("{job_title}", job_title)

        response = hh.make_http_request(
            "GET",
            url=base_url,
            params=query_params,
            headers=http_request.headers,
            timeout=10,
        )

        result = response.json()
        job_list = job_list.__add__(result["jobSearchResponse"]["data"])

        total_items = result["jobSearchResponse"]["meta"]["paging"]["total"]
        last_page_number = round(total_items / 15, 0)

        # fh.save_string_into_file(response.text, f"{page_number+1} - {job_title}.json")

        page_number = page_number + 1

    last_page_number = 1
    page_number = 0

    return job_list


def scrap_all_job_details_from_website(job_list):

    print(f"Total founditgulf job count: {len(job_list)}")

    job_details_list = []

    for job in job_list:
        job_details_list.append(scrap_job_details(job.get("id")))
        print(f"Fetched founditgulf job count: {len(job_details_list)}", end="\r")

    print(f"Fetched founditgulf job count: {len(job_details_list)}")
    return job_details_list


def scrap_job_details(job_id):

    curl_command = """
    curl 'https://www.founditgulf.com/middleware/jobdetail/{job_id}' \
    -H 'authority: www.founditgulf.com' \
    -H 'accept: application/json, text/plain, */*' \
    -H 'accept-language: en-US,en;q=0.9' \
    -H 'cookie: _gcl_au=1.1.83993725.1707209517; G_ENABLED_IDPS=google; WZRK_G=0154b99c518a432a8cb4d3d6542bcfbe; _fbp=fb.1.1707209518057.1578193184; ajs_anonymous_id=%2218d7d9ded6b752-0ad7e09f4b1418-4c657b58-157872-18d7d9ded6cd5b%22; NHP=true; MSUID=5d4b0fc9-5b6d-4832-81aa-42c079e89859; uuidAB=f8602a65-9651-451f-8af9-cbd0d28a32df; _ga=GA1.1.1275091489.1707209518; _ga_P9R1Y92J7R=GS1.2.1707224481.2.1.1707224492.49.0.0; _clck=zg7d0k%7C2%7Cfj3%7C0%7C1497; __gads=ID=fa9bcd912bc33673:T=1707222553:RT=1707370163:S=ALNI_MbClSQyISRduZKHH_6z834hOVfMMg; __gpi=UID=00000cfa86d57d60:T=1707222553:RT=1707370163:S=ALNI_Ma2iMvTUrMPxoZylW0V1HrGnOtwwg; __eoi=ID=dc01cbf2c7076e26:T=1707222553:RT=1707370163:S=AA-AfjY0ahpHv2j5J8hIzyYBxpIx; _uetsid=fc45c010c4cc11ee8ca2974b877b220b; _uetvid=fc45d430c4cc11ee9b8f9f2e4b390d47; WZRK_S_6K9-ZK8-ZZ6Z=%7B%22p%22%3A7%2C%22s%22%3A1707369801%2C%22t%22%3A1707370171%7D; _clsk=77l0bj%7C1707370172656%7C10%7C1%7Co.clarity.ms%2Fcollect; _ga_B3CBFFVVNQ=GS1.1.1707369798.10.1.1707370172.50.0.0; FCNEC=%5B%5B%22AKsRol9BoWz8JsEuqc1pqvXzNAO-ofAaafLbDcrOitqGZMAql9qHBLdcKInWrBePt-ePvdAHtlmKvaRDGhkImjFsjTeNG1-2WEjUTXkWyx1tQi0R1atuV_tAdb242EpDPoifHVE2ESBm-m4anDNGTl5rkpm2JlOG_Q%3D%3D%22%5D%5D' \
    -H 'referer: https://www.founditgulf.com/srp/results?query=Software+Developer&locations=Saudi+Arabia&searchId=05938aaa-99b7-4426-a017-f74db2932699' \
    -H 'sec-ch-ua: "Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"' \
    -H 'sec-ch-ua-mobile: ?0' \
    -H 'sec-ch-ua-platform: "Windows"' \
    -H 'sec-fetch-dest: empty' \
    -H 'sec-fetch-mode: cors' \
    -H 'sec-fetch-site: same-origin' \
    -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0' \
    -H 'x-language-code: EN' \
    -H 'x-source-country: SA' \
    -H 'x-source-site-context: monstergulf' \
    --compressed
    """

    http_request = hh.curl_to_requests(curl_command)
    base_url, query_params = hh.parse_query_params(http_request.url)

    response = hh.make_http_request(
        "GET",
        url=base_url.replace("{job_id}", job_id),
        headers=http_request.headers,
    )

    return response.json()
