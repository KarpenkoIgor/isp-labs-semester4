from json_parser.json_parser import Json
from pickle_parser.pickle_parser import Pickle
from toml_parser.toml_parser import Toml
from yaml_parser.yaml_parser import Yaml


class Serializer:
    def create_serializer(ext):
        if ext == ".json":
            return Json
        elif ext == ".toml":
            return Toml
        elif ext == ".yaml":
            return Yaml
        else:
            return Pickle