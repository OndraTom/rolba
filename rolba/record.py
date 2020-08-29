import jsonschema
from abc import ABC, abstractmethod
from typing import Dict


class Record(ABC):

    @abstractmethod
    def __eq__(self, other: "Record") -> bool:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class VinylRecord(Record):

    def __init__(self, name: str, price: float, link: str):
        self.name = name
        self.price = price
        self.link = link

    def __eq__(self, other: "VinylRecord") -> bool:
        return self.name == other.name and self.price == other.price and self.link == other.link

    def __str__(self) -> str:
        return f"{self.name} | {round(self.price)} Kč"

    def get_name(self) -> str:
        return self.name

    def get_price(self) -> float:
        return self.price

    def get_link(self) -> str:
        return self.link


class RecordFactory(ABC):

    @abstractmethod
    def create_from_dict(self, dict_record: dict) -> Record:
        pass


class VinylRecordFactory(RecordFactory):

    SCHEMA = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "minLength": 1
            },
            "price": {
                "type": "number",
                "minimum": 0
            },
            "link": {
                "type": "string",
                "minLength": 1
            }
        },
        "required": ["name", "price", "link"]
    }

    def create_from_dict(self, dict_record: dict) -> Record:
        try:
            jsonschema.validate(dict_record, self.SCHEMA)
            return VinylRecord(
                name=dict_record["name"],
                price=dict_record["price"],
                link=dict_record["link"]
            )
        except jsonschema.ValidationError:
            raise InvalidJsonSchemaError(dict_record)


class RecordDictMapper(ABC):

    @abstractmethod
    def get_mapped_record(self, record: Record) -> dict:
        pass


class VinylRecordDictMapper(RecordDictMapper):

    def get_mapped_record(self, record: VinylRecord) -> dict:
        return {
            "name": record.get_name(),
            "price": record.get_price(),
            "link": record.get_link()
        }


class RecordsCollection:

    def __init__(self):
        self.records: [Record] = []

    def get_records(self) -> [Record]:
        return self.records

    def add_record(self, record: Record) -> "RecordsCollection":
        if record not in self:
            self.records.append(record)
        return self

    def __len__(self) -> int:
        return len(self.records)

    def __eq__(self, other: "RecordsCollection") -> bool:
        if len(self.records) != len(other.get_records()):
            return False
        for record in self.records:
            if record not in other:
                return False
        return True

    def __contains__(self, item: Record) -> bool:
        for record in self.records:
            if record == item:
                return True
        return False

    def __sub__(self, other: "RecordsCollection") -> "RecordsCollection":
        self_hash_map = self._get_records_hash_map()
        other_hash_map = other._get_records_hash_map()
        diff_collection = RecordsCollection()
        for record_hash, record in self_hash_map.items():
            if record_hash not in other_hash_map:
                diff_collection.add_record(record)
        return diff_collection

    def _get_records_hash_map(self) -> Dict[str, Record]:
        return {str(record): record for record in self.records}


class RecordFactoryException(Exception):
    pass


class InvalidJsonSchemaError(RecordFactoryException):

    def __init__(self, given_json: dict):
        self.given_json = given_json

    def __str__(self) -> str:
        return f"Invalid json has been given: {self.given_json}"
