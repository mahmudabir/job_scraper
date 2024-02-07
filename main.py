import tanqeeb_job_scraping_helper as tanqeeb_helper


def main():
    search_urls = tanqeeb_helper.generate_search_urls()
    print(search_urls)


if __name__ == "__main__":
    print("\n")
    main()
