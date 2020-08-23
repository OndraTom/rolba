import os
from unittest import TestCase
from rolba.configuration import Configuration, ConfigurationFileNotFound, ConfigurationParsingError, \
    ConfigurationValidationError


class ConfigurationTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.fixtures_path = os.path.dirname(os.path.abspath(__file__)) + "/fixtures/config"

    def test_valid_config(self):
        config = Configuration(self.fixtures_path + "/valid_config.json")
        self.assertEqual(config.get_smtp_url(), "test smtp_url")
        self.assertEqual(config.get_emailing_user(), "test user")
        self.assertEqual(config.get_emailing_password(), "test password")

    def test_config_file_not_found_error(self):
        with self.assertRaises(ConfigurationFileNotFound):
            Configuration("invalid_path")

    def test_config_parsing_error(self):
        with self.assertRaises(ConfigurationParsingError):
            Configuration(self.fixtures_path + "/invalid_config.txt")

    def test_config_validation_error(self):
        with self.assertRaises(ConfigurationValidationError):
            Configuration(self.fixtures_path + "/invalid_config.json")
