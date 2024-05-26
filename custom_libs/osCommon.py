import os
from pathlib import Path


def create_file_path_string(list_of_dir):
    dir_path = Path(__file__).parents[1]

    for item in list_of_dir:
        dir_path = os.path.join(dir_path, item)

    return dir_path


def append_to_dir(dir_path, sub_to_add, **kwargs):
    if 'list' in kwargs:
        for dirName in sub_to_add:
            dir_path = os.path.join(dir_path, dirName)

        return dir_path

    return os.path.join(dir_path, sub_to_add)


def check_create_directory(dir_to_create):
    if not check_if_dir_exists(dir_to_create):
        create_dir(dir_to_create)


def check_if_dir_exists(dir_to_check):
    return os.path.isdir(dir_to_check)


def create_dir(dir_to_create):
    os.mkdir(dir_to_create)


def check_if_file_exists(file_to_check):
    return os.path.isfile(file_to_check)
