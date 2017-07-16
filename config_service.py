import os.path
import yaml


class ConfigService:
    def __init__(self, env):
        file_name = ConfigService.__get_file_name(env)

        with open(file_name, 'r') as file:
            self.cfg = yaml.safe_load(file)

    def get_section(self, section_name):
        if section_name not in self.cfg:
            return

        return self.cfg[section_name]

    @staticmethod
    def __get_file_name(env):
        default_file_name = 'config.yml'

        if env is not None:
            env_file_name = 'config_{}.yml'.format(env)
            if os.path.isfile(env_file_name):  # exists
                print('load environment configuration for "{}"'.format(env))
                return env_file_name

        print('load default configuration')
        return default_file_name
