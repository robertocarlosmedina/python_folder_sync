import os
import shutil
import hashlib
import time

from typing import Callable
from io import TextIOWrapper
from abc import ABC, abstractmethod

from src.sync_messages import sync_messages
from src.utils import check_folder_existent


class FolderSynchronizer(ABC):

    @abstractmethod
    def calculate_md5(file_path):
        md5_hasher = hashlib.md5()
        with open(file_path, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                md5_hasher.update(chunk)
        return md5_hasher.hexdigest()

    @abstractmethod
    def build_source_records(source_folder: str) -> set:
        file_records = set()
        for root, _, files in os.walk(source_folder):
            for file in files:
                file_path = os.path.relpath(
                    os.path.join(root, file), source_folder)
                file_records.add(file_path)
        return file_records

    @abstractmethod
    def handle_logs(log: TextIOWrapper, message, print_header=False) -> None:
        if print_header:
            log.write(f"{'-' * 50}\n")
            print(f"{'-' * 50}")
        log.write(f"{message}\n")
        print(message)

    @abstractmethod
    def handle_changes(log: TextIOWrapper, source: str, replica: str, log_function: Callable[..., None]) -> None:
        FolderSynchronizer.handle_logs(
            log, f"[INFO]: Sync started at {time.strftime('%Y-%m-%d %H:%M:%S')}", print_header=True)

        shutil.copy2(source, replica)

        FolderSynchronizer.handle_logs(
            log, log_function(source, replica))
        FolderSynchronizer.handle_logs(
            log, f"[INFO]: Sync completed at {time.strftime('%Y-%m-%d %H:%M:%S')}")

    @abstractmethod
    def sync_files(root: str, replica_root: str, file: str, log: TextIOWrapper) -> None:
        source_file_path = os.path.join(root, file)
        replica_file_path = os.path.join(replica_root, file)
        source_md5 = FolderSynchronizer.calculate_md5(source_file_path)

        if os.path.exists(replica_file_path):
            replica_md5 = FolderSynchronizer.calculate_md5(
                replica_file_path)
            if source_md5 != replica_md5:
                FolderSynchronizer.handle_changes(
                    log, source_file_path, replica_file_path, sync_messages["copy"])
            return

        FolderSynchronizer.handle_changes(
            log, source_file_path, replica_file_path, sync_messages["create"])

    @abstractmethod
    def sync_folders_records(log: TextIOWrapper, file_path: str, replica_folder_path: str):
        replica_full_path = os.path.join(replica_folder_path, file_path)
        if not os.path.exists(os.path.join(replica_folder_path, file_path)):
            if os.path.exists(replica_full_path):
                os.remove(replica_full_path)
                FolderSynchronizer.handle_changes(log, "source", replica_folder_path, sync_messages["delete"])

    @abstractmethod
    def sync_folders(source_folder_path, replica_folder_path, log_file_name):
        file_records = FolderSynchronizer.build_source_records(source_folder=source_folder_path)
        check_folder_existent(folder_name="Source",
                              folder_path=source_folder_path)
        check_folder_existent(
            folder_name="Replica", folder_path=replica_folder_path, create_if_not_existent=True)

        with open(f"./logs/{log_file_name}.log", "a") as log:
            for root, _, files in os.walk(source_folder_path):
                relative_path = os.path.relpath(root, source_folder_path)
                replica_root = os.path.join(replica_folder_path, relative_path)
                os.makedirs(replica_root, exist_ok=True)

                [FolderSynchronizer.sync_files(
                    root, replica_root, file, log) for file in files]

            [FolderSynchronizer.sync_folders_records(
                log=log, file_path=file_path, replica_folder_path=replica_folder_path) for file_path in file_records]
