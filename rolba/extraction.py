from abc import ABC, abstractmethod
from urllib.parse import urlsplit, urlparse
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.http.response import Response
from rolba.record import VinylRecord, RecordsCollection


class RecordsExtractor(ABC):
    pass


class WebSpider(Spider, ABC):

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
    }


class WebSpiderRecordsExtractor(RecordsExtractor, ABC):

    def __init__(self, crawler_process: CrawlerProcess):
        self.crawler_process = crawler_process
        self.records = RecordsCollection()
        self._register_spider()

    @abstractmethod
    def _register_spider(self):
        pass

    def get_records(self) -> RecordsCollection:
        return self.records


class VinylEmpireRecordsSpider(WebSpider):

    name = "Vinyl empire records spider"

    def __init__(self, **kwargs):
        super().__init__()
        self.start_urls = kwargs["args"]["start_urls"]
        self.data_read_callback = kwargs["args"]["data_read_callback"]

    def parse(self, response: Response, **kwargs):
        for product_container in response.css('div.product-container'):
            self.data_read_callback({
                'name': product_container.css('a.product-name ::text').get().strip(),
                'price': self._get_price_from_string(
                    product_container.css('span.product-price ::text').get().strip()
                ),
                'link': product_container.css('a.product-name ::attr(href)').get().strip()
            })
        next_page = response.css('li.pagination_next a::attr(href)').get()
        if next_page:
            request_url_split = urlsplit(response.request.url)
            yield response.follow(
                f"{request_url_split.scheme}://{request_url_split.netloc}{next_page}",
                self.parse
            )

    @staticmethod
    def _get_price_from_string(price_value: str) -> float:
        return float(price_value.split(" ")[0].replace(",", "."))


class VinylEmpireRecordsExtractor(WebSpiderRecordsExtractor):

    RECORDS_URL = "https://vinylempire.cz/13-bazarove-vinyly?id_category=13&n=60"

    def _register_spider(self):
        self.crawler_process.crawl(
            VinylEmpireRecordsSpider,
            args={
                "start_urls": [self.RECORDS_URL],
                "data_read_callback": lambda record: self.records.add_record(
                    VinylRecord(record["name"], record["price"], record["link"])
                )
            }
        )


class BlackVinylBazarRecordsSpider(WebSpider):

    name = "Black Vinyl Bazar records spider"

    page_param_name = "krit"

    def __init__(self, **kwargs):
        super().__init__()
        self.start_urls = kwargs["args"]["start_urls"]
        self.data_read_callback = kwargs["args"]["data_read_callback"]

    def parse(self, response: Response, **kwargs):
        is_empty_page = True
        for product_container in response.css('div.ramecekshop'):
            is_empty_page = False
            self.data_read_callback({
                'name': product_container.css('a.nadpisramecek ::text').get().strip(),
                'price': self._get_price_from_string(
                    product_container.css('a.objednejkosobr ::text').get().strip()
                ),
                'link': self._get_product_link(
                    response,
                    product_container.css('a.nadpisramecek ::attr(href)').get().strip()
                )
            })
        if not is_empty_page:
            yield response.follow(self._get_next_page_url(response), self.parse)

    @staticmethod
    def _get_price_from_string(price_value: str) -> float:
        return float(price_value.split("\xa0")[0].replace(",", "."))

    @staticmethod
    def _get_next_page_url(response: Response) -> str:
        current_url_split = response.request.url.split("-")
        current_url_split[-1] = str(int(current_url_split[-1]) + 1)
        return "-".join(current_url_split)

    @staticmethod
    def _get_product_link(response: Response, product_link: str) -> str:
        parsed_uri = urlparse(response.request.url)
        return f"{parsed_uri.scheme}://{parsed_uri.netloc}/{product_link}"


class BlackVinylBazarRecordsExtractor(WebSpiderRecordsExtractor):

    RECORDS_URL = "https://www.blackvinylbazar.cz/bazar?ids=2&krit=raz8-80-1"

    def _register_spider(self):
        self.crawler_process.crawl(
            BlackVinylBazarRecordsSpider,
            args={
                "start_urls": [self.RECORDS_URL],
                "data_read_callback": lambda record: self.records.add_record(
                    VinylRecord(record["name"], record["price"], record["link"])
                )
            }
        )


class VinylBazarRecordsSpider(WebSpider):

    name = "Vinyl Bazar records spider"

    def __init__(self, **kwargs):
        super().__init__()
        self.start_urls = kwargs["args"]["start_urls"]
        self.data_read_callback = kwargs["args"]["data_read_callback"]

    def parse(self, response: Response, **kwargs):
        for product_container in response.css('div.product'):
            self.data_read_callback({
                'name': product_container.css('div.productTitleContent a ::text').get().strip(),
                'price': self._get_price_from_string(
                    product_container.css('span.product_price_text ::text').get().strip()
                ),
                'link': self._get_base_url(response.request.url) + product_container.css(
                    'div.productTitleContent a ::attr(href)'
                ).get().strip()
            })
        next_page = response.css('div.pagination a.next ::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    @staticmethod
    def _get_price_from_string(price_value: str) -> float:
        return float(price_value.split("\xa0")[0].replace(",", "."))

    @staticmethod
    def _get_base_url(url: str):
        parsed_uri = urlparse(url)
        return f"{parsed_uri.scheme}://{parsed_uri.netloc}"


class VinylBazarRecordsExtractor(WebSpiderRecordsExtractor):

    RECORDS_URLS = [
        "https://www.vinylbazar.net/pop-rock-usa-uk",
        "https://www.vinylbazar.net/soul-funk-disco",
        "https://www.vinylbazar.net/breakbeat",
        "https://www.vinylbazar.net/downtempo-chillout",
        "https://www.vinylbazar.net/jazz-blues-usa-uk",
        "https://www.vinylbazar.net/country-folk",
        "https://www.vinylbazar.net/etnicka-hudba"
    ]

    def _register_spider(self):
        self.crawler_process.crawl(
            VinylBazarRecordsSpider,
            args={
                "start_urls": self.RECORDS_URLS,
                "data_read_callback": lambda record: self.records.add_record(
                    VinylRecord(record["name"], record["price"], record["link"])
                )
            }
        )


class LpBazarRecordsSpider(WebSpider):

    name = "LP Bazar records spider"

    def __init__(self, **kwargs):
        super().__init__()
        self.start_urls = kwargs["args"]["start_urls"]
        self.data_read_callback = kwargs["args"]["data_read_callback"]

    def parse(self, response: Response, **kwargs):
        for product_container in response.css('div.product'):
            availability = product_container.css("span.p-cat-availability ::text").get().strip()
            if not availability.startswith("Skladem"):
                continue
            self.data_read_callback({
                'name': product_container.css('a.p-name span ::text').get().strip(),
                'price': self._get_price_from_string(
                    product_container.css('span.p-det-main-price ::text').get().strip()
                ),
                'link': self._get_base_url(response.request.url) + product_container.css(
                    'a.p-name ::attr(href)'
                ).get().strip()[1:]
            })
        next_page = response.css('div.pagination a.s-page.pagination-page ::attr(href)').get()
        if next_page:
            request_url_split = urlsplit(response.request.url)
            yield response.follow(
                f"{request_url_split.scheme}://{request_url_split.netloc}{next_page}",
                self.parse
            )

    @staticmethod
    def _get_price_from_string(price_value: str) -> float:
        return float(price_value.split(" ")[0].replace(",", "."))

    @staticmethod
    def _get_base_url(url: str):
        parsed_uri = urlparse(url)
        return f"{parsed_uri.scheme}://{parsed_uri.netloc}/"


class LpBazarRecordsExtractor(WebSpiderRecordsExtractor):

    RECORDS_URL = "https://www.lpbazar.cz/lp-desky/"

    def _register_spider(self):
        self.crawler_process.crawl(
            LpBazarRecordsSpider,
            args={
                "start_urls": [self.RECORDS_URL],
                "data_read_callback": lambda record: self.records.add_record(
                    VinylRecord(record["name"], record["price"], record["link"])
                )
            }
        )
