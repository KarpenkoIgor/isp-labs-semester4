import dill as pickle


class Pickle:

    def dump(obj, file="testpickle.pickle"):
        with open(file, "wb+") as fw:
            pickle.dump(obj, fw)

    def dumps(obj):
        return pickle.dumps(obj)

    def load(file="testpickle.pickle"):
        with open(file, "rb+") as fr:
            obj = fr.read()
        return pickle.loads(obj)

    def loads(src):
        return pickle.loads(src)