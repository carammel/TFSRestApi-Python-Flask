import yaml

class GetAccess(object):
    def __init__(self):
        with open('src\config.yaml', 'r') as config_file:
            self.content = yaml.load(config_file)

    def parse_yaml(self, key_1, key_2):
        key_1 = key_1
        key_2 = key_2
        return self.content[key_1][key_2]
