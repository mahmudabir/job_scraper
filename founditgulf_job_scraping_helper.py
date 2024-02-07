import requests

import helpers.csv_helper as ch
import helpers.file_helper as fh
import helpers.json_helper as jh
from main import searching_job_titles
from models.job_details import JobDetails

job_details_list_json_file_name = "founditgulf_job_details_list.json"
job_list_json_file_name = "founditgulf_job_list.json"

job_details_list_csv_file_name = "founditgulf_job_details_list.csv"

is_caching_enabled = False


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
        fh.save_string_into_file(
            jh.data_to_json_string(job_details_list), job_details_list_json_file_name
        )
    else:
        job_details_list = jh.json_string_to_data(job_details_list_string)

    return job_details_list


def scrap_job_list_from_website():
    job_list = []

    cookies = {
        "_gcl_au": "1.1.83993725.1707209517",
        "G_ENABLED_IDPS": "google",
        "WZRK_G": "0154b99c518a432a8cb4d3d6542bcfbe",
        "_fbp": "fb.1.1707209518057.1578193184",
        "ajs_anonymous_id": "%2218d7d9ded6b752-0ad7e09f4b1418-4c657b58-157872-18d7d9ded6cd5b%22",
        "NHP": "true",
        "MSUID": "5d4b0fc9-5b6d-4832-81aa-42c079e89859",
        "uuidAB": "f8602a65-9651-451f-8af9-cbd0d28a32df",
        "_ga": "GA1.1.1275091489.1707209518",
        "_ga_P9R1Y92J7R": "GS1.2.1707224481.2.1.1707224492.49.0.0",
        "_clck": "zg7d0k%7C2%7Cfj2%7C0%7C1497",
        "__gads": "ID=fa9bcd912bc33673:T=1707222553:RT=1707328407:S=ALNI_MbClSQyISRduZKHH_6z834hOVfMMg",
        "__gpi": "UID=00000cfa86d57d60:T=1707222553:RT=1707328407:S=ALNI_Ma2iMvTUrMPxoZylW0V1HrGnOtwwg",
        "__eoi": "ID=dc01cbf2c7076e26:T=1707222553:RT=1707328407:S=AA-AfjY0ahpHv2j5J8hIzyYBxpIx",
        "_uetsid": "fc45c010c4cc11ee8ca2974b877b220b",
        "_uetvid": "fc45d430c4cc11ee9b8f9f2e4b390d47",
        "FCNEC": "%5B%5B%22AKsRol_ulLKMQoe57Pqsr1PtggOh1LYNhlBdm0wnhnHIGxuVhWg_k-30sj7I96qCP81iCn5_ryx8VmzEmye5NIEOM-wK2sEpf6LcWXwUkF7gducKH4Ujp_mkJ4kg0e37r_tlOxQvw3Uan0ytTAZFT29NVuhz6rYI8A%3D%3D%22%5D%5D",
        "WZRK_S_6K9-ZK8-ZZ6Z": "%7B%22s%22%3A1707327662%2C%22t%22%3A1707328489%2C%22p%22%3A3%7D",
        "_ga_B3CBFFVVNQ": "GS1.1.1707327663.8.1.1707328491.29.0.0",
        "_clsk": "5s7vp2%7C1707328491231%7C18%7C1%7Cz.clarity.ms%2Fcollect",
    }

    headers = {
        "authority": "www.founditgulf.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        # 'cookie': '_gcl_au=1.1.83993725.1707209517; G_ENABLED_IDPS=google; WZRK_G=0154b99c518a432a8cb4d3d6542bcfbe; _fbp=fb.1.1707209518057.1578193184; ajs_anonymous_id=%2218d7d9ded6b752-0ad7e09f4b1418-4c657b58-157872-18d7d9ded6cd5b%22; NHP=true; MSUID=5d4b0fc9-5b6d-4832-81aa-42c079e89859; uuidAB=f8602a65-9651-451f-8af9-cbd0d28a32df; _ga=GA1.1.1275091489.1707209518; _ga_P9R1Y92J7R=GS1.2.1707224481.2.1.1707224492.49.0.0; _clck=zg7d0k%7C2%7Cfj2%7C0%7C1497; __gads=ID=fa9bcd912bc33673:T=1707222553:RT=1707328407:S=ALNI_MbClSQyISRduZKHH_6z834hOVfMMg; __gpi=UID=00000cfa86d57d60:T=1707222553:RT=1707328407:S=ALNI_Ma2iMvTUrMPxoZylW0V1HrGnOtwwg; __eoi=ID=dc01cbf2c7076e26:T=1707222553:RT=1707328407:S=AA-AfjY0ahpHv2j5J8hIzyYBxpIx; _uetsid=fc45c010c4cc11ee8ca2974b877b220b; _uetvid=fc45d430c4cc11ee9b8f9f2e4b390d47; FCNEC=%5B%5B%22AKsRol_ulLKMQoe57Pqsr1PtggOh1LYNhlBdm0wnhnHIGxuVhWg_k-30sj7I96qCP81iCn5_ryx8VmzEmye5NIEOM-wK2sEpf6LcWXwUkF7gducKH4Ujp_mkJ4kg0e37r_tlOxQvw3Uan0ytTAZFT29NVuhz6rYI8A%3D%3D%22%5D%5D; WZRK_S_6K9-ZK8-ZZ6Z=%7B%22s%22%3A1707327662%2C%22t%22%3A1707328489%2C%22p%22%3A3%7D; _ga_B3CBFFVVNQ=GS1.1.1707327663.8.1.1707328491.29.0.0; _clsk=5s7vp2%7C1707328491231%7C18%7C1%7Cz.clarity.ms%2Fcollect',
        "referer": "https://www.founditgulf.com/srp/results?start=15&sort=1&limit=15&query=Software%20Engineer&locations=Saudi%20Arabia&queryDerived=true",
        "sec-ch-ua": '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
        "x-language-code": "EN",
        "x-source-country": "SA",
        "x-source-site-context": "monstergulf",
    }

    params = {
        "start": 0,
        "sort": "1",
        "limit": "15",
        "query": "",
        "locations": "Saudi Arabia",
        "queryDerived": "true",
    }

    for job_title in searching_job_titles:
        job_list = job_list.__add__(
            fetch_jobs_by_job_title(job_title, cookies, headers, params)
        )

    return [job for job in job_list if job.get("type") is None]


def fetch_jobs_by_job_title(job_title: str, cookies, headers, params):

    last_page_number = 1
    page_number = 0

    # job_title_base = job_title
    # job_title = job_title.lower().replace(" ", "+")

    job_list = []

    while page_number <= last_page_number:

        params["start"] = page_number * 15
        params["query"] = job_title
        # params["queryEntity"] = params["queryEntity"].replace("{job_title}", job_title)

        response = requests.get(
            "https://www.founditgulf.com/middleware/jobsearch",
            params=params,
            cookies=cookies,
            headers=headers,
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

    print(f"Total job count: {len(job_list)}")

    job_details_list = []

    for job in job_list:
        job_details_list.append(scrap_job_details(job.get("id")))
        print(f"Fetched job count: {len(job_details_list)}", end="\r")

    print(f"Fetched job count: {len(job_details_list)}")
    return job_details_list


def scrap_job_details(job_id):

    cookies = {
        "_gcl_au": "1.1.83993725.1707209517",
        "G_ENABLED_IDPS": "google",
        "WZRK_G": "0154b99c518a432a8cb4d3d6542bcfbe",
        "_fbp": "fb.1.1707209518057.1578193184",
        "ajs_anonymous_id": "%2218d7d9ded6b752-0ad7e09f4b1418-4c657b58-157872-18d7d9ded6cd5b%22",
        "NHP": "true",
        "MSUID": "5d4b0fc9-5b6d-4832-81aa-42c079e89859",
        "uuidAB": "f8602a65-9651-451f-8af9-cbd0d28a32df",
        "_ga": "GA1.1.1275091489.1707209518",
        "_ga_P9R1Y92J7R": "GS1.2.1707224481.2.1.1707224492.49.0.0",
        "_clck": "zg7d0k%7C2%7Cfj2%7C0%7C1497",
        "__gads": "ID=fa9bcd912bc33673:T=1707222553:RT=1707331174:S=ALNI_MbClSQyISRduZKHH_6z834hOVfMMg",
        "__gpi": "UID=00000cfa86d57d60:T=1707222553:RT=1707331174:S=ALNI_Ma2iMvTUrMPxoZylW0V1HrGnOtwwg",
        "__eoi": "ID=dc01cbf2c7076e26:T=1707222553:RT=1707331174:S=AA-AfjY0ahpHv2j5J8hIzyYBxpIx",
        "_uetsid": "fc45c010c4cc11ee8ca2974b877b220b",
        "_uetvid": "fc45d430c4cc11ee9b8f9f2e4b390d47",
        "FCNEC": "%5B%5B%22AKsRol9CX3uskIqs29d8pJ33jSpwSE1Ufb2OFsIonjAtVlC_r1OEfsLRSfYlJz_Kr5U1fqI1zokLMMu0Y9rNT5a4rW5OSNEeGu9IOSTqk0hCQwE4Dkz5rypATrKowraeNV37m9eSKnWi6BioH0ad7z2OlfQFeRMM2w%3D%3D%22%5D%5D",
        "WZRK_S_6K9-ZK8-ZZ6Z": "%7B%22p%22%3A7%2C%22s%22%3A1707330769%2C%22t%22%3A1707331227%7D",
        "_clsk": "5s7vp2%7C1707331228862%7C34%7C1%7Cz.clarity.ms%2Fcollect",
        "_ga_B3CBFFVVNQ": "GS1.1.1707330769.9.1.1707331229.3.0.0",
    }

    headers = {
        "authority": "www.founditgulf.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        # 'cookie': '_gcl_au=1.1.83993725.1707209517; G_ENABLED_IDPS=google; WZRK_G=0154b99c518a432a8cb4d3d6542bcfbe; _fbp=fb.1.1707209518057.1578193184; ajs_anonymous_id=%2218d7d9ded6b752-0ad7e09f4b1418-4c657b58-157872-18d7d9ded6cd5b%22; NHP=true; MSUID=5d4b0fc9-5b6d-4832-81aa-42c079e89859; uuidAB=f8602a65-9651-451f-8af9-cbd0d28a32df; _ga=GA1.1.1275091489.1707209518; _ga_P9R1Y92J7R=GS1.2.1707224481.2.1.1707224492.49.0.0; _clck=zg7d0k%7C2%7Cfj2%7C0%7C1497; __gads=ID=fa9bcd912bc33673:T=1707222553:RT=1707331174:S=ALNI_MbClSQyISRduZKHH_6z834hOVfMMg; __gpi=UID=00000cfa86d57d60:T=1707222553:RT=1707331174:S=ALNI_Ma2iMvTUrMPxoZylW0V1HrGnOtwwg; __eoi=ID=dc01cbf2c7076e26:T=1707222553:RT=1707331174:S=AA-AfjY0ahpHv2j5J8hIzyYBxpIx; _uetsid=fc45c010c4cc11ee8ca2974b877b220b; _uetvid=fc45d430c4cc11ee9b8f9f2e4b390d47; FCNEC=%5B%5B%22AKsRol9CX3uskIqs29d8pJ33jSpwSE1Ufb2OFsIonjAtVlC_r1OEfsLRSfYlJz_Kr5U1fqI1zokLMMu0Y9rNT5a4rW5OSNEeGu9IOSTqk0hCQwE4Dkz5rypATrKowraeNV37m9eSKnWi6BioH0ad7z2OlfQFeRMM2w%3D%3D%22%5D%5D; WZRK_S_6K9-ZK8-ZZ6Z=%7B%22p%22%3A7%2C%22s%22%3A1707330769%2C%22t%22%3A1707331227%7D; _clsk=5s7vp2%7C1707331228862%7C34%7C1%7Cz.clarity.ms%2Fcollect; _ga_B3CBFFVVNQ=GS1.1.1707330769.9.1.1707331229.3.0.0',
        "referer": "https://www.founditgulf.com/srp/results?start=90&sort=1&limit=15&query=Software+Engineer&locations=Saudi+Arabia&queryDerived=true&searchId=abc46d3a-5736-4df0-a95b-2129a890fcb8",
        "sec-ch-ua": '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
        "x-language-code": "EN",
        "x-source-country": "SA",
        "x-source-site-context": "monstergulf",
    }

    response = requests.get(
        f"https://www.founditgulf.com/middleware/jobdetail/{job_id}",
        cookies=cookies,
        headers=headers,
        timeout=5,
    )

    return response.json()
