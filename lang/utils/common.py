import os
from pathlib import Path

def lookup_table(*coll):
    return {value: True  for i, value in enumerate(coll)}

def spit(file_path, data):
    with open(file_path, 'w', encoding='utf8') as file:
        file.write(data)

def cat(file_path):
    pass


def read_chars(path: Path):
    """
    Read file char by char    
    :param path: path of file
    :type path: Path
    """
    with open(path, 'r', encoding='utf-8') as file:
        return list(file.read())

