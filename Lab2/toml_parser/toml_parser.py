import pytomlpp
from Utilities.Utilities import convert, deconvert


class Toml:

    def dump(obj, file="testtoml.toml"):
        packed = convert(obj)
        with open(file, 'w+') as fw:
            pytomlpp.dump(packed, fw)

    def dumps(obj):
        packed = convert(obj)
        return pytomlpp.dumps(packed)

    def load(file="testtoml.toml"):
        with open(file, 'r+') as fr:
            packed = pytomlpp.load(fr)
        return deconvert(packed)

    def loads(src):
        packed = pytomlpp.loads(src)
        return deconvert(packed)