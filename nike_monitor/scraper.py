from typing import Any

import requests

from .countries import countries
from .custom_exceptions import CountryNotFound


class Scraper:
    BASE_URL = "https://api.nike.com/product_feed/threads/v3"

    def __init__(self, country_code: str, upcoming: str = "true"):
        self.country_code = country_code.upper()
        self.upcoming = upcoming
    
    def create_api_url(self) -> str:
        language = countries.get(self.country_code, "")
        if language == "":
            raise CountryNotFound(f"The given country({self.country_code}) has not been found!")
        return f"{self.BASE_URL}/?anchor=0&count=50&filter=marketplace%28{self.country_code}%29&filter=language%28{language}%29&filter=upcoming%28{self.upcoming}%29&filter=channelId%28010794e5-35fe-4e32-aaff-cd2c74f89d61%29&filter=exclusiveAccess%28true%2Cfalse%29&sort=effectiveStartSellDateAsc"

    def fetch(self) -> dict[str, Any]:
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
        }
        res = requests.get(
            self.create_api_url(),
            headers=headers
        )
        json_res = res.json()
        return json_res.get("objects", {})
