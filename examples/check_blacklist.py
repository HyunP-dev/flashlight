import hashlib

from flashlight.checkitonion import CheckItOnion
from flashlight.ahmia import get_banned


def main():
    blacklist = get_banned()
    for site in CheckItOnion().topsites:
        md5 = hashlib.md5(site.url.encode()).hexdigest()
        if md5 in blacklist:
            if site.is_running:
                print(site.url, site.title, sep="\t")


if __name__ == "__main__":
    main()
