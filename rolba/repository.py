import os
import json
from abc import ABC, abstractmethod
from rolba.record import RecordsCollection, RecordFactory, RecordDictMapper


class RecordsRepository(ABC):

    @abstractmethod
    def save_records(self, records: RecordsCollection):
        pass

    @abstractmethod
    def load_records(self) -> RecordsCollection:
        pass


class JsonFileRecordsRepository(RecordsRepository):

    def __init__(self, file_path: str, record_factory: RecordFactory, record_dict_mapper: RecordDictMapper):
        self.file_path = file_path
        self.record_factory = record_factory
        self.record_dict_mapper = record_dict_mapper
        # Ensuring the directory existence
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)

    def save_records(self, records: RecordsCollection):
        with open(self.file_path, "w") as f:
            f.write(
                json.dumps(
                    [self.record_dict_mapper.get_mapped_record(r) for r in records.get_records()]
                )
            )

    def load_records(self) -> RecordsCollection:
        """
        :raises InvalidJsonError: if the file contains an invalid JSON
        :raises RecordFactoryException: if the record creation fails
        """
        records_collection = RecordsCollection()
        if not os.path.isfile(self.file_path):
            return records_collection
        try:
            with open(self.file_path) as f:
                for record in json.load(f):
                    records_collection.add_record(
                        self.record_factory.create_from_dict(record)
                    )
            return records_collection
        except json.JSONDecodeError:
            raise InvalidJsonError


class RecordsRepositoryException(Exception):
    pass


class JsonFileRecordsRepositoryException(RecordsRepositoryException):
    pass


class InvalidJsonError(JsonFileRecordsRepositoryException):

    def __str__(self) -> str:
        return "JSON repository file content is not valid"
