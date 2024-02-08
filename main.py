import founditgulf_job_scraping_helper

searching_job_titles = ["software engineer", "software developer"]


def main():

    founditgulf_job_scraping_helper.is_caching_enabled = False
    founditgulf_job_scraping_helper.start_scraping()

    # curl_command = """
    #     curl 'https://www.founditgulf.com/middleware/jobsearch?start=15&sort=1&limit=15&query=Software%20Developer&locations=Saudi%20Arabia&queryDerived=true' \
    #     -H 'authority: www.founditgulf.com' \
    #     -H 'accept: application/json, text/plain, */*' \
    #     -H 'accept-language: en-US,en;q=0.9' \
    #     -H 'cookie: _gcl_au=1.1.83993725.1707209517; G_ENABLED_IDPS=google; WZRK_G=0154b99c518a432a8cb4d3d6542bcfbe; _fbp=fb.1.1707209518057.1578193184; ajs_anonymous_id=%2218d7d9ded6b752-0ad7e09f4b1418-4c657b58-157872-18d7d9ded6cd5b%22; NHP=true; MSUID=5d4b0fc9-5b6d-4832-81aa-42c079e89859; uuidAB=f8602a65-9651-451f-8af9-cbd0d28a32df; _ga=GA1.1.1275091489.1707209518; _ga_P9R1Y92J7R=GS1.2.1707224481.2.1.1707224492.49.0.0; _clck=zg7d0k%7C2%7Cfj3%7C0%7C1497; _uetsid=fc45c010c4cc11ee8ca2974b877b220b; _uetvid=fc45d430c4cc11ee9b8f9f2e4b390d47; FCNEC=%5B%5B%22AKsRol-HRpVfwdLcC-5nm8bER81NgignGasUuAlt2hYfd_ADqp9S7ci-5LwsHFbiJuP9CSs3Lynp7JdHki0IYDg6XjbtFpmgoJesnqCxVhR8eCSnKwu4ENsB-XJ50amqZltkeHpYC9P64WoV_M7g6c5Q_OJTwlaEPA%3D%3D%22%5D%5D; _clsk=77l0bj%7C1707372142782%7C13%7C1%7Co.clarity.ms%2Fcollect; __gads=ID=fa9bcd912bc33673:T=1707222553:RT=1707372143:S=ALNI_MbClSQyISRduZKHH_6z834hOVfMMg; __gpi=UID=00000cfa86d57d60:T=1707222553:RT=1707372143:S=ALNI_Ma2iMvTUrMPxoZylW0V1HrGnOtwwg; __eoi=ID=dc01cbf2c7076e26:T=1707222553:RT=1707372143:S=AA-AfjY0ahpHv2j5J8hIzyYBxpIx; _ga_B3CBFFVVNQ=GS1.1.1707369798.10.1.1707372144.60.0.0' \
    #     -H 'referer: https://www.founditgulf.com/srp/results?start=15&sort=1&limit=15&query=Software%20Developer&locations=Saudi%20Arabia&queryDerived=true' \
    #     -H 'sec-ch-ua: "Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"' \
    #     -H 'sec-ch-ua-mobile: ?0' \
    #     -H 'sec-ch-ua-platform: "Windows"' \
    #     -H 'sec-fetch-dest: empty' \
    #     -H 'sec-fetch-mode: cors' \
    #     -H 'sec-fetch-site: same-origin' \
    #     -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0' \
    #     -H 'x-language-code: EN' \
    #     -H 'x-source-country: SA' \
    #     -H 'x-source-site-context: monstergulf' \
    #     --compressed
    #     """

    # request_value_code = convert_to_requests.curl_to_python_code(curl_command)
    # request_value_request = convert_to_requests.curl_to_requests(curl_command)

    # headers, params, cookies = hh.curl_to_requests(curl_command)

    # print(f"request_value_code: \n {request_value_code}")
    # print()
    # print(f"request_value_request: \n {request_value_request}")
    # print()

    # response = requests.get(url=request_value_request.url, params=request_value_request)

    # print(f"Headers: {headers}\n")
    # print(f"Params: {params}\n")
    # print(f"Cookies: {cookies}\n")

    # print()


if __name__ == "__main__":
    print("\n")
    print("Operation Started\n")
    main()
    print("\n")
    print("Operation Completed\n")
