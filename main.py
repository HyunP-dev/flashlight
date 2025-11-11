from typing import *
import requests
from bs4 import BeautifulSoup
import urllib.parse
from hashlib import md5


PROXIES = {
    "http": "socks5h://127.0.0.1:9150",
    "https": "socks5h://127.0.0.1:9150"
}


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


def is_nsfw(raw) -> bool:
    # TODO: NSFW Content Detection
    return True


def main():
    with open("hidden-wiki-url.txt") as f:
        wiki_url = f.read().strip()

    wiki_html = requests.get(url=wiki_url, proxies=PROXIES).text

    for link in get_onion_links(wiki_html):
        netloc = urllib.parse.urlparse(link).netloc
        print(netloc, md5(netloc.encode()).digest().hex(), sep="\t")

        for image_url in get_image_srcs(link):
            req = requests.get(url=image_url, proxies=PROXIES)
            raw = req.content

            if not is_nsfw(raw):
                continue
            
            filename = image_url.split("/")[-1]
            md5_ = md5(raw).digest().hex()

            print(filename, md5_, sep="\t")


if __name__ == "__main__":
    main()
