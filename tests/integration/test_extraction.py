import os
import shutil
from unittest import TestCase, mock
from scrapy.crawler import CrawlerProcess
from rolba.record import VinylRecordFactory, VinylRecordDictMapper
from rolba.repository import JsonFileRecordsRepository
from rolba.extraction import VinylEmpireRecordsExtractor, BlackVinylBazarRecordsExtractor
from rolba.worker import WebSpiderExtractionsProcessor


class WebSpiderExtractionsProcessorTest(TestCase):

    TEST_STORAGE_DIR_PATH = os.path.dirname(os.path.abspath(__file__)) + "/storage"

    @classmethod
    def setUpClass(cls) -> None:
        if os.path.isdir(cls.TEST_STORAGE_DIR_PATH):
            shutil.rmtree(cls.TEST_STORAGE_DIR_PATH)
        os.mkdir(cls.TEST_STORAGE_DIR_PATH)

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.TEST_STORAGE_DIR_PATH)

    def test_extraction(self):
        crawler_process = CrawlerProcess()
        WebSpiderExtractionsProcessor(
            crawler_process=crawler_process,
            records_collections_notifier=mock.Mock()
        ).register_extraction(
            title="Vinyl Empire",
            extractor=VinylEmpireRecordsExtractor(
                crawler_process=crawler_process
            ),
            repository=JsonFileRecordsRepository(
                file_path=self.TEST_STORAGE_DIR_PATH + "/vinyl_empire_records.json",
                record_factory=VinylRecordFactory(),
                record_dict_mapper=VinylRecordDictMapper()
            )
        ).register_extraction(
            title="Black Vinyl Bazar",
            extractor=BlackVinylBazarRecordsExtractor(
                crawler_process=crawler_process
            ),
            repository=JsonFileRecordsRepository(
                file_path=self.TEST_STORAGE_DIR_PATH + "/black_vinyl_bazar_records.json",
                record_factory=VinylRecordFactory(),
                record_dict_mapper=VinylRecordDictMapper()
            )
        ).run()
        self.assertTrue(
            os.path.isfile(self.TEST_STORAGE_DIR_PATH + "/vinyl_empire_records.json")
        )
        self.assertTrue(
            os.path.isfile(self.TEST_STORAGE_DIR_PATH + "/black_vinyl_bazar_records.json")
        )
