"""Module providing classess to construct data sources"""

import configparser

config = configparser.ConfigParser()
config.read("datasources.ini")

class DataSourceConfig:
    """Class representing a section of a datasource config"""

    def __init__(self, datasource_config, section = None, keys_to_validate = None) -> None:
        self.type = None
        self.keys_to_validate = keys_to_validate
        self.section = section
        self.config = datasource_config
        self.datasource_config = self.config[self.section]

    def get_type(self):
        """Returns the datasource type of the given section"""
        return self.section.get("type")

    def set_section(self, section):
        """Set the section of the object"""
        self.section = section

    def set_keys_to_validate(self, keys) -> list:
        """Set the keys (as a list) to validate agains section"""
        self.keys_to_validate = keys

    def validate(self):
        """Validates the givens keys agains section"""
        for key in self.keys_to_validate:
            if not self.config.has_option(self.section, key):
                print(key)
                return False
