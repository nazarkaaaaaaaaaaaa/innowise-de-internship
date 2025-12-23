import logging
import re
from typing import Any
import gc

phone_pattern = r"phone=\+?\d\-?\s?\(?\d{1,3}\s?\)?\-?\d{3}\s?\-?\d{2}\s?\-?\d{2}"
email_pattern = r"email=[A-Za-z0-9]+(\.?-?\+?[A-Za-z0-9]+)*@[a-zA-Z0-9]+(\.[a-z]{2,6})?(\.[a-z]{2,3})+"
token_pattern = r"token=(bearer\_?\s?)?eyJhbGciOiJIUzI1Ni[A-Za-z0-9]*J9.[A-Za-z0-9\.]+"

def read_data(filepath) -> list[str]:
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            lines = []
            for line in file:
                lines.append(line)
            return lines
    except FileNotFoundError:
        print(f"File {filepath} not found")

def find_and_replace(line) -> dict[str, Any]:
    phone_changes, phone_count = re.subn(phone_pattern, "<PHONE>", line)
    email_changes, email_count = re.subn(email_pattern, "<EMAIL>", phone_changes)
    token_changes, token_count = re.subn(token_pattern, "<TOKEN>", email_changes)
    return {
        "line": token_changes,
        "phone_count": phone_count,
        "email_count": email_count,
        "token_count": token_count
    }

def write_data(filepath, lines):
    with (open(filepath, "w", encoding="utf-8") as file):
        for index, line in enumerate(lines):
            result = find_and_replace(line)
            file.write(result.get("line"))
            logging.info(f"Line {index + 1}: "
                f"Phones: {result.get('phone_count')} replaces, "
                f"Emails: {result.get('email_count')} replaces, "
                f"Tokens: {result.get('token_count')} replaces")
            if (result.get("phone_count") +
                result.get("email_count")) + result.get("token_count") > 4:
                logging.warning(f"Line {index + 1} has more than 4 replaces")

logging.basicConfig(
    filename="masker.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

if __name__ == "__main__":
    lines = read_data("user_events1.txt")
    write_data("user_events.txt", lines)
    collected = gc.collect()
    print(f"Garbage collector ran, {collected} unreachable objects found and deleted.")
