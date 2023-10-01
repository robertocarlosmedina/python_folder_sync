import os
import sys


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
