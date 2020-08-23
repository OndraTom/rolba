from typing import Tuple, List
from scrapy.crawler import CrawlerProcess
from rolba.record import RecordsCollection
from rolba.extraction import RecordsExtractor
from rolba.repository import RecordsRepository
from rolba.notification import RecordsCollectionsNotifier


class WebSpiderExtractionsProcessor:

    def __init__(self, crawler_process: CrawlerProcess, records_collections_notifier: RecordsCollectionsNotifier):
        self.crawler_process = crawler_process
        self.records_collections_notifier = records_collections_notifier
        self.extractions: List[Tuple[str, RecordsExtractor, RecordsRepository]] = []

    def register_extraction(self, title: str, extractor: RecordsExtractor, repository: RecordsRepository) \
            -> "WebSpiderExtractionsProcessor":
        self.extractions.append(
            (title, extractor, repository)
        )
        return self

    def run(self):
        self.crawler_process.start()
        records_collections: List[Tuple[str, RecordsCollection]] = []
        for (title, extractor, repository) in self.extractions:
            new_records = extractor.get_records()
            saved_records = repository.load_records()
            repository.save_records(new_records)
            records_collections.append((title, new_records - saved_records))
        self.records_collections_notifier.send_notification(records_collections)
