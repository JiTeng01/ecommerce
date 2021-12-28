import os
import json


def delete_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)


def has_file(file_path):
    return os.path.isfile(file_path)


def list_files(file_path):
    return os.listdir(file_path)


def has_directory(directory):
    return os.path.exists(directory)


def create_directory(directory):
    if not has_directory(directory):
        os.makedirs(directory)


def split_extension(filename):
    return os.path.splitext(filename)


def read_json(path):
    with open(path, "r") as handler:
        return json.loads(handler.read())


def write_json(path, data):
    with open(path, "w") as handler:
        handler.write(json.dumps(data))
