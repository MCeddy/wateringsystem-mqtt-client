import yaml


class ConfigService:
    def __init__(self):
        with open('config.yml', 'r') as file:
            self.cfg = yaml.safe_load(file)

    def get_section(self, section_name):
        if section_name not in self.cfg:
            return

        return self.cfg[section_name]
