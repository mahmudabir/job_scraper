import bayt_job_scraping_helper
import constants

# import founditgulf_job_scraping_helper


def main():
    constants.is_caching_enabled = False

    # founditgulf_job_scraping_helper.start_scraping()

    bayt_job_scraping_helper.start_scraping()

    # string = ".NET Software Engineer, .NET 8, C# - Digital Downloads  - Saudi Arabia"
    # generated_string = bayt_job_scraping_helper.generate_job_path_parameter(
    #     string, "123456789"
    # )
    # print(string)
    # print(generated_string)


if __name__ == "__main__":
    print("\n")
    print("Operation Started\n")
    main()
    print("\n")
    print("Operation Completed\n")
