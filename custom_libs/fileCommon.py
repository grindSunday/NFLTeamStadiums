import json


def write_json_string_to_file(fpath, jayson):
    with open(fpath, 'w') as f:
        f.writelines(jayson)


def load_json_from_file(fpath):
    with open(fpath, 'r') as f:
        try:
            op_json = json.load(f)
        except json.decoder.JSONDecodeError:
            op_json = dict()

    return op_json


def dump_json_to_file(fpath, jayson_dict_or_list_of_dicts):
    with open(fpath, 'w') as f:
        json.dump(jayson_dict_or_list_of_dicts, f)


def write_content_to_file(f_name, content):
    with open(f_name, 'w', encoding='utf-8') as f:
        f.write(content)


def read_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

    return file_content

