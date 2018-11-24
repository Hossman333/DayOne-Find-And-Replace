import os
import json
import argparse


def parse_cmd_args():
    parser = argparse.ArgumentParser(
        description="Find and replace text for Day One JSON exports.")
    parser.add_argument(
        "--file-in", help="Input source for a single JSON file.")

    parser.add_argument(
        "--folder-in", help="Input source for a directory full of JSON files.")

    parser.add_argument(
        "--word-replaced", required=True, help="Word to be replaced.")

    parser.add_argument(
        "--word-replacing", required=True, help="Word that is replacing.")

    return parser.parse_args()


def get_attribute(data, attribute, default_value):
    return data.get(attribute) or default_value


def update_single_file(path_to_json, json_file_name, word_to_be_replaced,
                       word_replacing):
    with open(path_to_json + "/" + json_file_name, "r") as raw_data:
        json_data = json.load(raw_data)
        for entries in json_data["entries"]:
            # In case the entry doesn't have the field "text".
            data_to = get_attribute(entries, 'text', None)
            if not data_to:
                continue
            else:
                entries["text"] = entries["text"].replace(
                    word_to_be_replaced, word_replacing)

    updated_file_name = json_file_name.split(".")[0] + "(updated).json"
    with open(path_to_json + "/" + updated_file_name, "w") as fout:
        fout.write(json.dumps(json_data))


def folder_iteration(path_to_json, word_to_be_replaced, word_replacing):
    json_files = [
        pos_json for pos_json in os.listdir(path_to_json)
        if pos_json.endswith('.json')
    ]

    for single_file in json_files:
        update_single_file(path_to_json, single_file, word_to_be_replaced,
                           word_replacing)


def file_iteration(path_to_json, word_to_be_replaced, word_replacing):
    file_name = path_to_json.split("/")[-1]
    updated_path_to_json = path_to_json.split("/")
    del updated_path_to_json[-1]
    updated_path_to_json = '/'.join(updated_path_to_json)

    update_single_file(updated_path_to_json, file_name, word_to_be_replaced,
                       word_replacing)


def main():
    args = parse_cmd_args()

    word_to_be_replaced = args.word_replaced
    word_replacing = args.word_replacing

    if not (args.folder_in or args.file_in):
        print(
            "==================================================================="
        )
        print(
            'No action requested, add --folder-in or --file-in. Type -h for help'
        )
        print(
            "==================================================================="
        )
    else:
        if args.folder_in is not None:
            path_to_json = args.folder_in
            folder_iteration(path_to_json, word_to_be_replaced, word_replacing)
        else:
            path_to_json = args.file_in
            if (path_to_json.endswith('.json')):
                file_iteration(path_to_json, word_to_be_replaced,
                               word_replacing)
            else:
                print(
                    "==================================================================="
                )
                print(
                    'Invalid file requested, Must be a single file of type JSON. Type -h for help'
                )
                print(
                    "==================================================================="
                )


if __name__ == "__main__":
    main()
