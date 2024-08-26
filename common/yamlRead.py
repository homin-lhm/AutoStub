from main import DIR, ENVIRON
import yaml


class YamlRead:
    @staticmethod
    def env_config():
        """环境变量的读取方式"""
        with open(file=f'{DIR}/config/env/{ENVIRON}/config.yml', mode='r', encoding='utf-8') as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    @staticmethod
    def data_config():
        with open(file=f'{DIR}/config/data/config.yml', mode='r', encoding='utf-8') as f:
            return yaml.load(f, Loader=yaml.FullLoader)
