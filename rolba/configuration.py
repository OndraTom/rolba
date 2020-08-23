import json
import jsonschema


class Configuration:

    JSON_SCHEMA = {
        "type": "object",
        "properties": {
            "emailing": {
                "type": "object",
                "properties": {
                    "smtp_url": {"type": "string"},
                    "user": {"type": "string"},
                    "password": {"type": "string"}
                },
                "required": [
                    "smtp_url", "user", "password"
                ]
            }
        },
        "required": [
            "emailing"
        ]
    }

    def __init__(self, config_file_path: str):
        try:
            with open(config_file_path) as config_file:
                self.config = json.load(config_file)
            jsonschema.validate(self.config, self.JSON_SCHEMA)
        except FileNotFoundError:
            raise ConfigurationFileNotFound(config_file_path)
        except json.JSONDecodeError:
            raise ConfigurationParsingError
        except jsonschema.ValidationError:
            raise ConfigurationValidationError

    def get_smtp_url(self) -> str:
        return self.config["emailing"]["smtp_url"]

    def get_emailing_user(self) -> str:
        return self.config["emailing"]["user"]

    def get_emailing_password(self) -> str:
        return self.config["emailing"]["password"]


class ConfigurationException(Exception):
    pass


class ConfigurationFileNotFound(ConfigurationException):

    def __init__(self, config_file_path: str):
        self.config_file_path = config_file_path

    def __str__(self) -> str:
        return f"Configuration file ({self.config_file_path}) hasn't been found"


class ConfigurationParsingError(ConfigurationException):

    def __str__(self) -> str:
        return "Configuration file content is not a valid JSON"


class ConfigurationValidationError(ConfigurationException):

    def __str__(self) -> str:
        return "Configuration is not valid"
