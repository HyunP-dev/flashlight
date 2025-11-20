import requests
from hashlib import md5

from flashlight.scrapper import *
from flashlight.model import is_nsfw


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
