import re


def read_file_by(path: str) -> str:
    """
    It reads the file at the given path, and if it doesn't exist, it creates new file at given path
    """
    try:
        with open(path, "r+", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        with open(path, "w", encoding="utf-8") as file:
            file.write("")
            return ""

def append_to_file(path: str, content: str) -> None:
    """
    Append the given content to the file at the given path.
    """
    with open(path, "a+", encoding="utf-8") as file:
        file.write("\n")
        file.write(content)

# def validate_webhook(url: str) -> bool:
#     """
#     It checks if the webhook URL seems to be valid(idk if its work perfectly)
#     """
#     return bool(re.match(r"^https://discord.com/api/webhooks/\d{18}/\w{68}", url))
