import requests


__cache = []


def get_banned(from_cache=True) -> list[str]:
    global __cache
    if from_cache and __cache:
        return __cache
    banned_list_url = "https://ahmia.fi/blacklist/banned/"
    __cache = requests.get(
        banned_list_url, headers={"user-agent": "Mozilla/5.0"}
    ).text.split()
    return __cache
