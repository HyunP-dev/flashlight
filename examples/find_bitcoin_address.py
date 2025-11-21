import re

from flashlight.scrapper import traverse_hrefs

pattern = re.compile(
    r"\b(?:[13][a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[0-9ac-hj-np-z]{6,87})\b"
)


def main():
    url = ""
    for url, bs in traverse_hrefs(url):
        for match in pattern.findall(str(bs)):
            print(f"{url} ===> {match}")


if __name__ == "__main__":
    main()
