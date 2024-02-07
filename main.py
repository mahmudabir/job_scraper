import founditgulf_job_scraping_helper

searching_job_titles = ["software engineer", "software developer"]


def main():

    founditgulf_job_scraping_helper.is_caching_enabled = False
    founditgulf_job_scraping_helper.start_scraping()


if __name__ == "__main__":
    print("\n")
    print("Operation Started\n")
    main()
    print("\n")
    print("Operation Completed\n")
