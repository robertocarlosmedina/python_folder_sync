import os
import re
import shutil

from typing import Callable
from io import TextIOWrapper
from abc import ABC, abstractmethod

from src.sync_messages import sync_messages
from src.utils import check_folder_existent, calculate_md5


class FolderSynchronizer(ABC):

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
    def handle_logs(log: TextIOWrapper, message) -> None:
        clean_message = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', message)
        log.write(f"{clean_message}\n")
        print(message)

    @abstractmethod
    def handle_changes(log: TextIOWrapper, source: str, replica: str, log_function: Callable[..., None]) -> None:
        shutil.copy2(source, replica)
        FolderSynchronizer.handle_logs(
            log, log_function(source, replica))

    @abstractmethod
    def sync_files(root: str, replica_root: str, file: str, log: TextIOWrapper) -> None:
        source_file_path = os.path.join(root, file)
        replica_file_path = os.path.join(replica_root, file)
        source_md5 = calculate_md5(source_file_path)

        if os.path.exists(replica_file_path):
            replica_md5 = calculate_md5(
                replica_file_path)
            if source_md5 != replica_md5:
                FolderSynchronizer.handle_changes(
                    log, source_file_path, replica_file_path, sync_messages["copy"])
            return

        FolderSynchronizer.handle_changes(
            log, source_file_path, replica_file_path, sync_messages["create"]["file"])

    @abstractmethod
    def sync_folders_records(log: TextIOWrapper, file_path: str, source_folder_path: str, replica_folder_path: str):
        replica_full_path = os.path.join(replica_folder_path, file_path)
        if not os.path.exists(os.path.join(source_folder_path, file_path)):
            if os.path.exists(replica_full_path):
                os.remove(replica_full_path)
                FolderSynchronizer.handle_logs(
                    log, sync_messages["delete"]["file"](file_path))

    @abstractmethod
    def sync_sub_folder(log: TextIOWrapper, root: str, replica_root: str, folder_path: str, replica_folder_path: str) -> None:
        source_folder_path = os.path.join(root, folder_path)
        replica_dir_path = os.path.join(replica_root, folder_path)
        if not os.path.exists(source_folder_path):
            if os.path.exists(replica_dir_path):
                shutil.rmtree(replica_dir_path)
                FolderSynchronizer.handle_logs(
                    log, sync_messages["delete"]["folder"](replica_root))

    @abstractmethod
    def check_replica_folder(log: TextIOWrapper, source_folder_path: str, replica_root: str) -> None:
        try:
            os.makedirs(replica_root)
            FolderSynchronizer.handle_logs(
                log, sync_messages["create"]["folder"](replica_root))
        except:
            pass

    @abstractmethod
    def sync_folders(source_folder_path, replica_folder_path, log_file_name):
        file_records = FolderSynchronizer.build_source_records(
            source_folder=replica_folder_path)
        check_folder_existent(folder_name="Source",
                              folder_path=source_folder_path)
        check_folder_existent(
            folder_name="Replica", folder_path=replica_folder_path, create_if_not_existent=True)

        with open(f"./logs/{log_file_name}.log", "a") as log:
            for root, _, files in os.walk(source_folder_path):
                relative_path = os.path.relpath(root, source_folder_path)
                replica_root = os.path.join(replica_folder_path, relative_path)
                FolderSynchronizer.check_replica_folder(
                    log=log, source_folder_path=source_folder_path, replica_root=replica_root)

                [FolderSynchronizer.sync_files(
                    root, replica_root, file, log) for file in files]

                for _, folders, _ in os.walk(replica_folder_path):
                    [FolderSynchronizer.sync_sub_folder(
                        log=log,
                        root=root,
                        replica_root=replica_root,
                        folder_path=folder,
                        replica_folder_path=replica_folder_path) for folder in folders]

            [FolderSynchronizer.sync_folders_records(
                log=log,
                file_path=file_path,
                source_folder_path=source_folder_path,
                replica_folder_path=replica_folder_path) for file_path in file_records]
