from unittest import TestCase
from rolba.record import VinylRecord, VinylRecordFactory, InvalidJsonSchemaError, \
    VinylRecordDictMapper, RecordsCollection


class VinylRecordTest(TestCase):

    def test_equality(self):
        self.assertEqual(
            VinylRecord("a", 1, "l"),
            VinylRecord("a", 1, "l")
        )
        self.assertNotEqual(
            VinylRecord("a", 1, "l"),
            VinylRecord("b", 2, "l"),
        )


class VinylRecordFactoryTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.factory = VinylRecordFactory()

    def test_create_from_json_success(self):
        self.assertIsInstance(
            self.factory.create_from_dict(
                {"name": "a", "price": 1, "link": "l"}
            ),
            VinylRecord
        )

    def test_creation_from_invalid_schema(self):
        with self.assertRaises(InvalidJsonSchemaError):
            self.factory.create_from_dict({})
        with self.assertRaises(InvalidJsonSchemaError):
            self.factory.create_from_dict({"name": "", "price": 1, "link": "l"})
        with self.assertRaises(InvalidJsonSchemaError):
            self.factory.create_from_dict({"name": "a", "price": -1, "link": "l"})


class VinylRecordJsonMapperTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.mapper = VinylRecordDictMapper()

    def test_mapping(self):
        self.assertEqual(
            self.mapper.get_mapped_record(
                VinylRecord("a", 1, "l")
            ),
            {"name": "a", "price": 1, "link": "l"}
        )


class RecordsCollectionTest(TestCase):

    def test_contains(self):
        collection = RecordsCollection().add_record(
            VinylRecord("a", 1, "l")
        )
        self.assertIn(
            VinylRecord("a", 1, "l"),
            collection
        )
        self.assertNotIn(
            VinylRecord("a", 2, "l"),
            collection
        )

    def test_equality(self):
        self.assertEqual(
            RecordsCollection().add_record(
                VinylRecord("a", 1, "l")
            ),
            RecordsCollection().add_record(
                VinylRecord("a", 1, "l")
            )
        )
        self.assertNotEqual(
            RecordsCollection().add_record(
                VinylRecord("a", 1, "l")
            ),
            RecordsCollection().add_record(
                VinylRecord("a", 2, "l")
            )
        )

    def test_subtraction(self):
        self.assertEqual(
            RecordsCollection().add_record(
                VinylRecord("a", 1, "l")
            ).add_record(
                VinylRecord("b", 2, "l")
            )
            -
            RecordsCollection().add_record(
                VinylRecord("a", 1, "l")
            ),
            RecordsCollection().add_record(
                VinylRecord("b", 2, "l")
            )
        )
        self.assertEqual(
            RecordsCollection().add_record(
                VinylRecord("a", 1, "l")
            ).add_record(
                VinylRecord("b", 2, "l")
            )
            -
            RecordsCollection().add_record(
                VinylRecord("c", 1, "l")
            ),
            RecordsCollection().add_record(
                VinylRecord("a", 1, "l")
            ).add_record(
                VinylRecord("b", 2, "l")
            )
        )
