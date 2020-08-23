from unittest import TestCase
from rolba.record import VinylRecord, VinylRecordFactory, InvalidJsonSchemaError, \
    VinylRecordDictMapper, RecordsCollection


class VinylRecordTest(TestCase):

    def test_equality(self):
        self.assertEqual(
            VinylRecord("a", 1),
            VinylRecord("a", 1)
        )
        self.assertNotEqual(
            VinylRecord("a", 1),
            VinylRecord("b", 2),
        )


class VinylRecordFactoryTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.factory = VinylRecordFactory()

    def test_create_from_json_success(self):
        self.assertIsInstance(
            self.factory.create_from_dict(
                {"name": "a", "price": 1}
            ),
            VinylRecord
        )

    def test_creation_from_invalid_schema(self):
        with self.assertRaises(InvalidJsonSchemaError):
            self.factory.create_from_dict({})
        with self.assertRaises(InvalidJsonSchemaError):
            self.factory.create_from_dict({"name": "", "price": 1})
        with self.assertRaises(InvalidJsonSchemaError):
            self.factory.create_from_dict({"name": "a", "price": -1})


class VinylRecordJsonMapperTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.mapper = VinylRecordDictMapper()

    def test_mapping(self):
        self.assertEqual(
            self.mapper.get_mapped_record(
                VinylRecord("a", 1)
            ),
            {"name": "a", "price": 1}
        )


class RecordsCollectionTest(TestCase):

    def test_contains(self):
        collection = RecordsCollection().add_record(
            VinylRecord("a", 1)
        )
        self.assertIn(
            VinylRecord("a", 1),
            collection
        )
        self.assertNotIn(
            VinylRecord("a", 2),
            collection
        )

    def test_equality(self):
        self.assertEqual(
            RecordsCollection().add_record(
                VinylRecord("a", 1)
            ),
            RecordsCollection().add_record(
                VinylRecord("a", 1)
            )
        )
        self.assertNotEqual(
            RecordsCollection().add_record(
                VinylRecord("a", 1)
            ),
            RecordsCollection().add_record(
                VinylRecord("a", 2)
            )
        )

    def test_subtraction(self):
        self.assertEqual(
            RecordsCollection().add_record(
                VinylRecord("a", 1)
            ).add_record(
                VinylRecord("b", 2)
            )
            -
            RecordsCollection().add_record(
                VinylRecord("a", 1)
            ),
            RecordsCollection().add_record(
                VinylRecord("b", 2)
            )
        )
        self.assertEqual(
            RecordsCollection().add_record(
                VinylRecord("a", 1)
            ).add_record(
                VinylRecord("b", 2)
            )
            -
            RecordsCollection().add_record(
                VinylRecord("c", 1)
            ),
            RecordsCollection().add_record(
                VinylRecord("a", 1)
            ).add_record(
                VinylRecord("b", 2)
            )
        )
