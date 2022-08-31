import random
import time
from typing import Any

from .release import Release
from .scraper import Scraper
from .webhook import send_webhook


class Monitor:
    def __init__(self, webhook_url: str, country_code: str, upcoming: str = "true"):
        self.webhook_url = webhook_url
        self.country_code = country_code.upper()
        self.upcoming = upcoming
        self.scraper = Scraper(self.country_code, self.upcoming)

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
        releases = self.scraper.fetch()

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

    def run(self):
        print(f"RUNNING [{self.country_code}] MONITOR!")
        specified_releases = self.get_release_details()
        for specified_release in specified_releases:
            print(f"SENDING RELEASE DETAILS[{self.country_code}] TO WEBHOOK: sku - {specified_release.sku}")
            send_webhook(self.webhook_url, specified_release)
            time.sleep(random.uniform(2.5, 5.5))
