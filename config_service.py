import os
import yaml
import logging


class ConfigService:
    def __init__(self, env):
        self.__logger = logging.getLogger(__name__)
        self.__load_from_file(env)

    def __load_from_file(self, env):
        file_name = self.__get_file_name(env)
        config_path = os.path.join(os.getcwd(), 'config', file_name)

        with open(config_path, 'r') as file:
            self.__cfg = yaml.safe_load(file)

    def __get_file_name(self, env):
        if env is not None:
            env_file_name = 'config_{}.yml'.format(env)
            
            if os.path.isfile(env_file_name):  # exists
                self.__logger.debug('load environment configuration for "{}"'.format(env))
                return env_file_name

        self.__logger.debug('load default configuration')
        return 'config.yml'

    def get_section(self, section_name):
        if section_name not in self.__cfg:
            return

        return self.__cfg[section_name]
