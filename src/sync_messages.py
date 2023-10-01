import time
from termcolor import colored


def get_time() -> None:
    return colored(f"{time.strftime('%Y-%m-%d %H:%M:%S')}", 'light_yellow')


sync_messages: dict = {
    "create": {
        "file": lambda source, replica: f"{get_time()} {colored('CREATE', 'green', attrs=['bold'])} File '{source}' from source created into replica '{replica}'",
        "folder": lambda replica: f"{get_time()} {colored('CREATE', 'green', attrs=['bold'])} Folder created in '{replica}' to sync source"
    },
    "copy": lambda source, replica: f"{get_time()} {colored('COPY', 'blue', attrs=['bold'])} Contents of file '{source}' from source copied to replica '{replica}'",
    "delete": {
        "file": lambda replica: f"{get_time()} {colored('DELETE', 'red', attrs=['bold'])} File deleted fom '{replica}' that doesn't exist in source",
        "folder": lambda replica: f"{get_time()} {colored('DELETE', 'red', attrs=['bold'])} Folder deleted fom '{replica}' that doesn't exist in source"
    }
}
