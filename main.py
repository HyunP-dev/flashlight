from typing import *
from io import BytesIO
import requests
from bs4 import BeautifulSoup
import urllib.parse
from hashlib import md5
from PIL import Image
from transformers import pipeline

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
    img = Image.open(BytesIO(raw))
    classifier = pipeline("image-classification",
                          model="Falconsai/nsfw_image_detection")
    for e in classifier(img):
        if e["label"] == "nsfw":
            if e["score"] > 0.8:
                return True
    return False


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

            filename = image_url.split("/")[-1]
            md5_ = md5(raw).digest().hex()
            if is_nsfw(raw):
                print(filename, md5_, sep="\t")


if __name__ == "__main__":
    main()
