"""Github and data handler module."""
import re

import requests


RAW_PUBLIC_APIS_URL = (
    "https://raw.githubusercontent.com/public-apis/public-apis/master/README.md"
)
ROW_REGEX = re.compile(
    r"\| +?(.+?) +?\| +?(.+?) +?\| +?(.+?) +?\| +?(.+?) +?\| +?(.+?) +?\|"
)
MARKDOWN_LINK_REGEX = re.compile(r"\[(.+?)\]\((.+?)\)")
MARKDOWN_LINK_EXCLUDE_REGEX = re.compile(r"\[.+?\]\(^#.+?\)")
REQUEST_TIMEOUT = 10


def yes_no_to_bool(value: str) -> bool:
    """Convert yes/no to bool.

    Args:
        value (str): Value to convert.

    Returns:
        bool: Converted value.
    """
    value = value.strip().lower()
    if "yes" in value:
        return True
    elif "no" in value:
        return False
    else:
        return None


def get_raw_public_apis() -> str:
    """Get raw public APIs from Github.

    Returns:
        str: Raw public APIs from Github.
    """
    resp = requests.get(RAW_PUBLIC_APIS_URL, timeout=REQUEST_TIMEOUT)
    text = resp.text
    return text


def parse_rows(raw_text: str) -> list:
    """Parse rows from raw text.

    Args:
        raw_text (str): Raw text to parse.

    Returns:
        list: List of parsed rows.
    """
    # Iterate over all of the headers for each of the sections
    # and then get all lines that are within a table under that
    # header that contain a link.
    apis = []

    category = None
    for line in raw_text.split("\n"):
        line = line.strip()

        # If we encounter a new category, update the category
        if line.startswith("### "):
            category = line.replace("### ", "").strip()

        # If we encounter a line that starts and ends with a pipe
        if (
            category is not None
            and ROW_REGEX.search(line) is not None
            and MARKDOWN_LINK_REGEX.search(line) is not None
            and MARKDOWN_LINK_EXCLUDE_REGEX.search(line) is None
        ):
            # Split the line by pipes
            parts = ROW_REGEX.findall(line)[0]
            # Get the link and description
            md_link, description = parts[0:2]
            # Get the name and link from the markdown link
            name, link = re.findall(MARKDOWN_LINK_REGEX, md_link)[0]
            # Determine auth method
            auth_method = parts[2].strip().lower().replace("`", "")
            if "oauth" in auth_method:
                auth_method = "oauth"
            elif "apikey" in auth_method or "api key" in auth_method:
                auth_method = "apikey"
            else:
                _auth_method = yes_no_to_bool(auth_method)
                if _auth_method is not None:
                    auth_method = _auth_method

            # Determine if HTTPS is supported
            https = parts[3].strip().lower()
            if "yes" in https:
                https = True
            else:
                https = False

            # Determine if CORS is supported
            cors = parts[4].strip().lower()
            if "yes" in cors:
                cors = True
            else:
                cors = False

            # Add the API to the list of APIs
            apis.append(
                {
                    "name": name,
                    "description": description,
                    "auth_method": auth_method,
                    "https": https,
                    "cors": cors,
                    "link": link,
                    "category": category,
                }
            )

    return apis
