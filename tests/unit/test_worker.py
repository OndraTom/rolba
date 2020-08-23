from unittest import TestCase, mock
from rolba.record import Record, RecordsCollection
from rolba.worker import WebSpiderExtractionsProcessor


class TestRecord(Record):

    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other: "TestRecord") -> bool:
        return self.name == other.name

    def __str__(self) -> str:
        return "Test Record"

    def get_name(self) -> str:
        return self.name


class WebSpiderExtractionsProcessorTest(TestCase):

    def test_run(self):
        crawler_process_mock = mock.Mock()
        notifier_mock = mock.Mock()
        extractor_mock = mock.Mock()
        repository_mock = mock.Mock()

        collection1 = RecordsCollection().add_record(
            TestRecord("test_record_1")
        ).add_record(
            TestRecord("test_record_2")
        )
        collection2 = RecordsCollection().add_record(
            TestRecord("test_record_2")
        ).add_record(
            TestRecord("test_record_3")
        )

        extractor_mock.get_records.return_value = collection1
        repository_mock.load_records.return_value = collection2

        self.assertIsNone(WebSpiderExtractionsProcessor(
            crawler_process=crawler_process_mock,
            records_collections_notifier=notifier_mock
        ).register_extraction(
            title="test",
            extractor=extractor_mock,
            repository=repository_mock
        ).run())

        crawler_process_mock.start.assert_called_once()
        notifier_mock.send_notification.assert_called_with(
            [("test", collection1 - collection2)]
        )
