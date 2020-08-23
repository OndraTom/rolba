import os
import shutil
import json
from unittest import TestCase
from rolba.record import Record, RecordFactory, RecordDictMapper, RecordsCollection
from rolba.repository import JsonFileRecordsRepository, InvalidJsonError


class TestRecord(Record):

    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other: "TestRecord") -> bool:
        return self.name == other.name

    def __str__(self) -> str:
        return "Test Record"

    def get_name(self) -> str:
        return self.name


class TestRecordFactory(RecordFactory):

    def create_from_dict(self, dict_record: dict) -> TestRecord:
        return TestRecord(dict_record["name"])


class TestRecordDictMapper(RecordDictMapper):

    def get_mapped_record(self, record: TestRecord) -> dict:
        return {"name": record.get_name()}


class JsonFileRecordsRepositoryTest(TestCase):

    STORAGE_PATH = os.path.dirname(os.path.abspath(__file__)) + "/test_storage"
    FIXTURES_PATH = os.path.dirname(os.path.abspath(__file__)) + "/fixtures/repository"

    @classmethod
    def setUpClass(cls) -> None:
        if os.path.isdir(cls.STORAGE_PATH):
            shutil.rmtree(cls.STORAGE_PATH)
        os.makedirs(cls.STORAGE_PATH)
        cls.record_factory = TestRecordFactory()
        cls.record_dict_mapper = TestRecordDictMapper()

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.STORAGE_PATH)

    def test_save_success(self):
        file_path = self.STORAGE_PATH + "/save_success.json"
        repository = JsonFileRecordsRepository(
            file_path=file_path,
            record_factory=self.record_factory,
            record_dict_mapper=self.record_dict_mapper
        )
        repository.save_records(
            RecordsCollection().add_record(
                TestRecord("test 1")
            ).add_record(
                TestRecord("test 2")
            )
        )
        self.assertTrue(
            os.path.isfile(file_path)
        )
        with open(file_path) as f:
            self.assertEqual(
                json.load(f),
                [
                    {"name": "test 1"},
                    {"name": "test 2"},
                ]
            )

    def test_load_success(self):
        records_collection = JsonFileRecordsRepository(
            file_path=self.FIXTURES_PATH + "/valid_repository.json",
            record_factory=self.record_factory,
            record_dict_mapper=self.record_dict_mapper
        ).load_records()
        self.assertIsInstance(records_collection, RecordsCollection)
        self.assertEqual(len(records_collection), 2)

    def test_invalid_json_load_error(self):
        with self.assertRaises(InvalidJsonError):
            JsonFileRecordsRepository(
                file_path=self.FIXTURES_PATH + "/invalid_repository.txt",
                record_factory=self.record_factory,
                record_dict_mapper=self.record_dict_mapper
            ).load_records()
