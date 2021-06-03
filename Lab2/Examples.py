import inspect

from JptySerializer.Serializer import Serializer


first_global = 3.14
second_global = 16
multiplier = 3


class Figure:
    name = "circle"

    def __init__(self, name):
        self.name = name
        self.radius = 5
        self.samples = ["prosto", "test", 1, 2, "rabotaet"]

    def square(self):
        return first_global * self.radius ** 2


def summing(a, b):
    res = a + b + second_global
    answer = f"Summing is {res}"
    return answer


def calculate(rad):
    # print("Now Harder")
    circ = Figure("little circle")
    circ.radius = rad
    squar = circ.square()
    differ = second_global

    def square_diff(square, difference):
        return square - difference

    difs = triple(square_diff(squar, differ))
    return summing(difs, circ.radius)


triple = lambda x: x * multiplier

circle = Figure("circle")
circle.radius = 12

json_seria = Serializer.create_serializer(".json")
pickle_seria = Serializer.create_serializer(".pickle")
toml_seria = Serializer.create_serializer(".toml")
yaml_seria = Serializer.create_serializer(".yaml")

met = yaml_seria.dump(calculate)
loaded = json_seria.load()
print(loaded(2))