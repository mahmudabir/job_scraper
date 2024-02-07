search_url: str = (
    "https://www.tanqeeb.com/jobs/search?"
    + "keywords={job_title}"
    + "&country=54"
    + "&state=0"
    + "&search_period=0"
    + "&order_by=most_recent"
    + "&search_in=f"
    + "&lang=all"
)

job_titles = ["Software Engineer", "Software Developer"]


def start_scraping():
    search_urls = generate_search_urls()
    print(search_urls)


def generate_search_urls():
    search_urls: list[str] = []

    for job_title in job_titles:
        new_url = search_url.replace("{job_title}", (job_title.replace(" ", "+")))
        search_urls.append(new_url)

    return search_urls
