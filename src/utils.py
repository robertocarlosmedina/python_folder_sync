import os
import sys
import hashlib


def check_folder_existent(folder_name: str, folder_path: str, create_if_not_existent=False) -> None:
    if not os.path.exists(folder_path):
        if create_if_not_existent:
            os.makedirs(folder_path)
            print(
                f"[INFO] {folder_name} folder '{folder_path}' does not exist\nInfo: {folder_name} folder '{folder_path}' created")
        else:
            print(
                f"[ERROR] {folder_name} folder '{folder_path}' does not exist\n")
            sys.exit(1)


def calculate_md5(file_path):
    md5_hasher = hashlib.md5()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            md5_hasher.update(chunk)
    return md5_hasher.hexdigest()
