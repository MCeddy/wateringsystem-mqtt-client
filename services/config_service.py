import os
import yaml
import logging


class ConfigService:
    def __init__(self, env):
        self.__logger = logging.getLogger(__name__)
        self.__load_from_file(env)

    def __load_from_file(self, env):
        config_path = self.__get_config_path(env)

        with open(config_path, 'r') as file:
            self.__cfg = yaml.safe_load(file)

    def __get_config_path(self, env):
        config_folder = os.path.join(os.getcwd(), 'config')

        if env is not None:
            env_file_name = 'config_{}.yml'.format(env)
            env_config_path = os.path.join(config_folder, env_file_name)
            
            if os.path.isfile(env_config_path):  # exists
                self.__logger.debug('load environment configuration for "{}"'.format(env))
                return env_config_path

        self.__logger.debug('load default configuration')
        config_path = os.path.join(config_folder, 'config.yml')
        return config_path

    def get_section(self, section_name):
        if section_name not in self.__cfg:
            return

        return self.__cfg[section_name]
