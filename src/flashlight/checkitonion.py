from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup


@dataclass
class Website:
    title: str
    url: str
    is_running: bool


class CheckItOnion:
    URL = "https://checkitonion.online/"
    HEADERS = {"user-agent": "Mozilla/5.0"}

    def __init__(self):
        self._topsites = []
        self.refresh()

    def refresh(self):
        html = requests.get(CheckItOnion.URL, headers=CheckItOnion.HEADERS).text
        bs = BeautifulSoup(html, "html5lib")
        left_div_elements = bs.select(".leftdiv")
        topsites_element = None
        for left_div in left_div_elements:
            if left_div.select_one(".div-topsites"):
                topsites_element = left_div
                break

        topsites = []
        if topsites_element:
            for element in topsites_element.select(".website-wrapper"):
                is_running = element.select_one(".status > span")["class"][0] == "up"
                title = element.select_one(".website-name").text
                url = element.select_one(".address").text
                topsites.append(Website(title, url, is_running))

        self._topsites = topsites

    @property
    def topsites(self) -> list[Website]:
        return self._topsites
