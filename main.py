# import bayt_job_scraping_helper
import constants

# import founditgulf_job_scraping_helper
import tanqeeb_job_scraping_helper


def main():
    constants.is_caching_enabled = False

    # founditgulf_job_scraping_helper.start_scraping()
    # bayt_job_scraping_helper.start_scraping()
    tanqeeb_job_scraping_helper.start_scraping()


if __name__ == "__main__":
    print("\n")
    print("Operation Started\n")
    main()
    print("\n")
    print("Operation Completed\n")
