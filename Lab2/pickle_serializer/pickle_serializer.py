import pickle
from additional.additional import convert, deconvert

class Pickle:
    def dump(self, obj, fp):
        return pickle.dump(convert(obj),open(fp,'wb'))

    def dumps(self, obj):
        return pickle.dumps(convert(obj))

    def load(self, fp):
        return deconvert(pickle.load(open(fp, 'rb')))

    def loads(self, s):
        return deconvert(pickle.loads(s))