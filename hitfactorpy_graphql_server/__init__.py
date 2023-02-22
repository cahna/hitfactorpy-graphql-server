from importlib.metadata import version
from os import path
from pathlib import Path

__version__ = version("hitfactorpy_graphql_server")
MODULE_ROOT = Path(path.dirname(path.abspath(__file__)))
