from abc import ABC, abstractmethod
import configparser

class DataSourceConfig:
    # Load the config ini file, if it exists
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
    
    def get_config(self):
        return self.config

    def get_types(self, type):
        ds_rest_list = [ds for ds in self.config.sections() if (self.config.get(ds, "type") == type)]
        return ds_rest_list

class DataSourceConfigValidator(ABC):
    def __init__(self, data_source_type) -> None:
        self.data_source_type = data_source_type

    @abstractmethod
    def validate_datasource_config(self):
        pass

class ValidatorRest(DataSourceConfigValidator):
    def __init__(self) -> None:
        super().__init__("rest")
        self.keys_to_validate = ["endpoint","http_verb","resource"]
        
    def validate_datasource_config(self, section, config):
        self.section = section
        self.config = config
        for key in self.keys_to_validate:
            if not self.config.has_option(self.section, key):
                print(key)
                return False
        return True