from typing import Dict, List, Optional

import requests

from webhook import send_webhook


class NikeStock:
    def __init__(self, country_code: str, language: str, upcoming: Optional[str] = "true"):
        self.base_url = "https://api.nike.com/product_feed/threads/v3"
        self.country_code = country_code
        self.language = language
        self.upcoming = upcoming

        self.session = requests.Session()
        self.session.headers.update({
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        })

    def get_json_page(self) -> List[Dict]:
        page = self.session.get(f"{self.base_url}/?anchor=0&count=50&filter=marketplace%28{self.country_code.upper()}%29&filter=language%28{self.language.lower()}%29&filter=upcoming%28{self.upcoming}%29&filter=channelId%28010794e5-35fe-4e32-aaff-cd2c74f89d61%29&filter=exclusiveAccess%28true%2Cfalse%29&sort=effectiveStartSellDateAsc")
        return page.json()['objects']

    def get_releases_infos(self) -> Dict:
        releases = {}
        json_page = self.get_json_page()
        for i in range(len(json_page)):
            sku = json_page[i]['productInfo'][0]['merchProduct']['styleColor']
            releases[sku] = {}
            releases[sku]['exclusiveAccess'] = json_page[i]['productInfo'][0]['merchProduct']['exclusiveAccess']
            releases[sku]['title'] = json_page[i]['productInfo'][0]['productContent']['title']
            releases[sku]['price'] = json_page[i]['productInfo'][0]['merchPrice']['fullPrice']
            releases[sku]['currency'] = json_page[i]['productInfo'][0]['merchPrice']['currency']
            releases[sku]['sizes'] = []
            try:
                releases[sku]['releaseType'] = json_page[i]['productInfo'][0]['launchView']['method']
            except KeyError:
                releases[sku]['releaseType'] = "TBA"
            try:
                releases[sku]['releaseDate'] = json_page[i]['productInfo'][0]['launchView']['startEntryDate']
            except KeyError:
                releases[sku]['releaseDate'] = "TBA"
            try:
                releases[sku]['image'] = json_page[i]['publishedContent']['nodes'][0]['nodes'][0]['properties']['portraitURL']
            except KeyError:
                releases[sku]['image'] = json_page[i]['publishedContent']['nodes'][0]['properties']['portraitURL']
            for j in range(len(json_page[i]['productInfo'][0]['skus'])):
                try:
                    stock = json_page[i]['productInfo'][0]['availableGtins'][j]['level']
                except (IndexError, KeyError):
                    stock = "TBA"
                try:
                    size = json_page[i]['productInfo'][0]['skus'][j]['countrySpecifications'][0]['localizedSize'] + json_page[i]['productInfo'][0]['skus'][j]['countrySpecifications'][0]['localizedSizePrefix']
                except KeyError:
                    size = json_page[i]['productInfo'][0]['skus'][j]['countrySpecifications'][0]['localizedSize']
                releases[sku]['sizes'].append(f"{stock} - {size}")
        send_webhook(releases)


if __name__ == "__main__":
    NikeStock("us","en").get_releases_infos()
