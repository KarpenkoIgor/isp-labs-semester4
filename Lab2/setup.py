from setuptools import setup

setup(
    name = "Lab2",
    version = "1.0",
    author = "Ihar Karpenka",
    author_email = "hv.karpenko@gmail.com",
    packages = ["additional", "factory", "my_json_serializer", 
        "pickle_serializer", "my_yaml_serializer",
        "my_toml_serializer"],
    scripts = ["serializer.py"]
)