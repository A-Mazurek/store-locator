from json import load
from typing import List, Dict


def read_file(file_name: str) -> List[Dict[str, str]]:
    """
        Get data from json file.
    """
    with open(file_name) as file:
        return load(file)
