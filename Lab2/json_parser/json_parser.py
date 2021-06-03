import json
from Utilities.Utilities import convert, deconvert


class Json:

    def dump(obj, file="testjson.json"):
        with open(file, 'w+') as fw:
            fw.write(Json.dumps(obj))

    def dumps(obj):
        packed = convert(obj)
        return json.dumps(packed)

    def load(file="testjson.json"):
        with open(file, 'r+') as fr:
            data = json.load(fr)
        unpacked = deconvert(data)
        return unpacked

    def loads(src):
        packed = json.loads(src)
        return deconvert(packed)