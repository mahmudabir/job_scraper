search_url: str = (
    "https://www.founditgulf.com/srp/results?"
    + "query={job_title}"
    + "&locations=Saudi+Arabia"
    + "&queryEntity={job_title}%3Adesignation"
    + "&searchId=84dfb99a-75c3-400e-932e-d9934dc798ec"
)

job_titles = ["software Engineer", "software Developer"]


def start_scraping():
    search_urls = generate_search_urls()

    for url in search_urls:
        print(url)


def generate_search_urls():
    search_urls: list[str] = []

    for job_title in job_titles:
        new_url = search_url.replace(
            "{job_title}", (job_title.lower().replace(" ", "+"))
        )
        search_urls.append(new_url)

    return search_urls
