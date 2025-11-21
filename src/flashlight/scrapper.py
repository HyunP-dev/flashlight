from typing import Generator

import requests
from bs4 import BeautifulSoup
import urllib.parse


PROXIES = {"http": "socks5h://127.0.0.1:9150", "https": "socks5h://127.0.0.1:9150"}


def get_onion_links(html) -> Generator[str, None, None]:
    bs = BeautifulSoup(html, "html5lib")
    for a in bs.select("a"):
        href = a["href"]
        if href.endswith(".onion"):
            yield href


def get_image_srcs(url) -> Generator[str, None, None]:
    # TODO: We need to modify this to work recursively.
    try:
        req = requests.get(url=url, proxies=PROXIES)
    except requests.exceptions.ConnectionError:
        return

    bs = BeautifulSoup(req.text, "html5lib")
    for img in bs.select("img"):
        image_url = urllib.parse.urljoin(url, img["src"])
        yield image_url


def traverse_hrefs(start_url: str) -> Generator[tuple[str, BeautifulSoup], None, None]:
    visited = set()

    def _iterate(url):
        if url in visited:
            return
        visited.add(url)
        try:
            html = requests.get(url, proxies=PROXIES).text
        except requests.exceptions.ConnectionError:
            return

        bs = BeautifulSoup(html, "html5lib")
        yield url, bs

        targets = set()
        for a in bs.select("a"):
            link = urllib.parse.urljoin(url, a["href"])

            if ".onion" in link and link.startswith(start_url):
                targets.add(link)

        for href in targets:
            for url, bs in _iterate(href):
                yield url, bs

    for url, bs in _iterate(start_url):
        yield url, bs
