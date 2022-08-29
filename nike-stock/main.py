import random
import time
from dataclasses import dataclass
from typing import Any

from scraper import Scraper
from webhook import send_webhook


@dataclass
class Release:
    sku: str
    exclusive_access: bool
    title: str
    price: float
    currency: str
    type: str
    date: str
    image: str
    sizes_with_stock: list[str]

class Monitor(Scraper):
    def __init__(self, country_code: str, upcoming: str = "true"):
        super().__init__(country_code, upcoming)

    def get_sizes_and_stock_details(self, release_detail: dict[str, Any]) -> list[str]:
        sizes_with_stock = []
        for idx, detail in enumerate(release_detail['skus']):
            try:
                stock = release_detail['availableGtins'][idx]['level']
            except (IndexError, KeyError):
                stock = "TBA"
            try:
                size = detail['countrySpecifications'][0]['localizedSize'] + detail['countrySpecifications'][0]['localizedSizePrefix']
            except KeyError:
                size = detail['countrySpecifications'][0]['localizedSize']
            sizes_with_stock.append(f"{stock} - {size}")
        return sizes_with_stock
    
    def get_release_details(self) -> list[Release]:
        specified_releases = []
        releases = self.fetch()

        release: dict[str, Any]
        for release in releases:
            release_detail: list[dict[str, Any]] = release.get('productInfo', [])
            if release_detail:
                sku = release_detail[0].get('merchProduct', {}).get('styleColor', '')
                exclusive_access = release_detail[0].get('merchProduct', {}).get('exclusiveAccess', '')
                title = release_detail[0].get('productContent', {}).get('title', '')
                price = release_detail[0].get('merchPrice', {}).get('fullPrice', 000)
                currency = release_detail[0].get('merchPrice', {}).get('currency', '')
                type = release_detail[0].get('launchView', {}).get('method', 'TBA')
                date = release_detail[0].get('launchView', {}).get('startEntryDate', 'TBA')
                sku = release_detail[0].get('merchProduct', {}).get('styleColor', '')
                try:
                    image = release['publishedContent']['nodes'][0]['nodes'][0]['properties']['portrait']['url']
                except KeyError:
                    image = release['publishedContent']['nodes'][0]['properties']['portraitURL']
                sizes_with_stock = self.get_sizes_and_stock_details(release_detail[0])
                specified_releases.append(
                    Release(
                        sku,
                        exclusive_access,
                        title,
                        price,
                        currency,
                        type,
                        date,
                        image,
                        sizes_with_stock
                    )
                )
        return specified_releases

    def main(self):
        specified_releases = self.get_release_details()
        for specified_release in specified_releases:
            send_webhook(specified_release)
            time.sleep(random.uniform(2.5, 5.5))


if __name__ == "__main__":
    monitor = Monitor("PL")
    essa = monitor.get_release_details()
    print(essa)
