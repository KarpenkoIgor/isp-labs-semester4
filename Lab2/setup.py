from distutils.core import setup

setup(
    name="my_parsers",
    version="1.0",
    description="Module for serializing(or deserializing) Json/Pickle/Toml/Yaml data",
    author="Ihar Karpenka",
    author_email="hv.karpenko@gmail.com",
    packages=["json_parser", "pickle_parser", "toml_parser", "yaml_parser",
              "utilities", "serializer"],
    install_requires=["dill", "pytomlpp", "pyyaml"],
    scripts=["app.py"]
)