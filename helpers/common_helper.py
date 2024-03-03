import msvcrt


def wait_for_key():
    msvcrt.getch()
    # while True:
    #     if msvcrt.kbhit():
    #         return msvcrt.getch()


def snake_to_space_case(snake_case_string):
    # Replace underscores with spaces
    space_case_string = snake_case_string.replace("_", " ")

    # Capitalize the first letter of each word
    space_case_string = space_case_string.title()

    return space_case_string
