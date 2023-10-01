import time
import sched
import argparse

from src.folder_synchronizer import FolderSynchronizer


args_parser = argparse.ArgumentParser()
args_parser.add_argument("-sr", "--source", required=True, type=str,
                         help="Please provide the Source file path")
args_parser.add_argument("-rp", "--replica", required=True, type=str,
                         help="Please provide the Replica file path")
args_parser.add_argument("-lg", "--log_file_name", required=True, type=str,
                         help="Please provide the Replica file path")
args_parser.add_argument("-ti", "--time_interval", required=True, type=str,
                         help="Please provide the Time Interval to Sync files in seconds")

sync_scheduler = sched.scheduler(time.time, time.sleep)


def sync_folders_scheduler(source_folder: str, replica_folder: str, log_file_name: str, time_interval: int):
    FolderSynchronizer.sync_folders(
        source_folder_path=source_folder,
        replica_folder_path=replica_folder,
        log_file_name=log_file_name)

    sync_scheduler.enter(
        delay=time_interval,
        priority=1,
        action=sync_folders_scheduler,
        argument=(source_folder, replica_folder, log_file_name, time_interval))


if __name__ == "__main__":
    print("\nPython Folder Sync")
    print("Waiting for changes...\n")
    args_parser_values = vars(args_parser.parse_args())

    sync_scheduler.enter(
        delay=0,
        priority=1,
        action=sync_folders_scheduler,
        argument=(args_parser_values["source"],
                  args_parser_values["replica"],
                  args_parser_values["log_file_name"],
                  int(args_parser_values["time_interval"])))

    sync_scheduler.run()
