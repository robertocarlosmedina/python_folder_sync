# Python Folder Sync

This project is has as it's main goal to synchronize two folders: source and
replica. The program can maintain a full, identical copy of source
folder at replica folder.

## Criteria's

- Synchronization must be one-way: after the synchronization content of the
  replica folder should be modified to exactly match content of the source
  folder;

- Synchronization should be performed periodically;

- File creation/copying/removal operations should be logged to a file and to the console output;

- Folder paths, synchronization interval and log file path should be provided
  using the command line arguments;

## Execute Project

### Check commands help

Run this script command to get help and description an all the other commands.

```shell

  python main.py -h

```

### Execute Folder Synchronization

One example on how to perform folder synchronization from a source file './source' to a replica file './replica', witch logs to a file with "example" with periodic time of 1 second.

```shell

  python main.py -sr ./source -rp ./replica -lg example -ti 1

```

## Log Labels

- CREATE - File/Folder creation event has been performed 
- COPY - File content copy event has been performed
- DELETE - File/Folder delete event has been performed 
