from yaml import load
import sys

class Configuration:
    def __init__(self, conf_file_location):
        try:
            with open(conf_file_location) as conf_file:
                conf_dict = load(conf_file)
            self.db = DBConfig(conf_dict['db'])
        except FileNotFoundError:
            print('Configuration File {} not found!'.format(conf_file_location))
            sys.exit(1)

class DBConfig:
    def __init__(self, db_config_dict):
        self.__dict__.update(db_config_dict)

if __name__ == '__main__':
    test_config = Configuration('./conf/configuration.yml')
    print(test_config.db.db_env_path)
