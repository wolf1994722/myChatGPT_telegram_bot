import os
import bardapi
from bardapi import Bard
from bardapi import BardCookies

def extract_bard_cookie(cookies: bool = False) -> dict:
    """
    Extracts the specified Bard cookie(s) from the browser's cookies.

    This function searches for the specified Bard cookies in various web browsers
    installed on the system. It supports modern web browsers and operating systems.

    Args:
        cookies (bool, optional): If False, extracts only '__Secure-1PSID' cookie.
            If True, extracts '__Secure-1PSID', '__Secure-1PSIDTS', and '__Secure-1PSIDCC' cookies.
            Defaults to False.

    Returns:
        dict: A dictionary containing the extracted Bard cookies.

    Raises:
        Exception: If no supported browser is found or if there's an issue with cookie extraction.
    """
    import browser_cookie3

    supported_browsers = [
        # browser_cookie3.chrome,
        # browser_cookie3.chromium,
        # browser_cookie3.opera,
        # browser_cookie3.opera_gx,
        # browser_cookie3.brave,
        # browser_cookie3.edge,
        # browser_cookie3.vivaldi,
        browser_cookie3.firefox,
        # browser_cookie3.librewolf,
        # browser_cookie3.safari,
    ]

    cookie_dict = {}

    for browser_fn in supported_browsers:
        try:
            cj = browser_fn(domain_name=".google.com")

            for cookie in cj:
                # if "io" in cookie.name:
                # print(cookie)
                # print(cookie)
                if cookie.name == "__Secure-1PSID" and cookie.value.endswith("."):
                    cookie_dict["__Secure-1PSID"] = cookie.value
                if cookies:
                    if cookie.name == "__Secure-1PSIDTS":
                        cookie_dict["__Secure-1PSIDTS"] = cookie.value
                    elif cookie.name == "__Secure-1PSIDCC":
                        cookie_dict["__Secure-1PSIDCC"] = cookie.value
                if len(cookie_dict) == 3:
                    return cookie_dict
        except Exception as e:
            # Ignore exceptions and try the next browser function
            continue

    if not cookie_dict:
        raise Exception("No supported browser found or issue with cookie extraction")

    # print(cookie_dict)
    return cookie_dict

cookie_dict = extract_bard_cookie(True)


bard = BardCookies(cookie_dict=cookie_dict)

def chatting(query):
    msg = bard.get_answer(query)['content']
    print(msg)
    return msg