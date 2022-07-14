"""
Provide multiprocess locking
"""
from os.path import exists
from pathlib import Path

import fcntl


class Locker:
    """
    Provides a multiprocess mutex
    https://stackoverflow.com/questions/6931342/system-wide-mutex-in-python-on-linux
    """

    lockfile_name = "lockfile.lck"

    def __init__(self):
        self.file_pointer = None

    def __enter__(self):
        if not exists(Locker.lockfile_name):
            Path(Locker.lockfile_name).touch()
        # we don't care about encoding for a lock file
        # pylint: disable=unspecified-encoding
        self.file_pointer = open(Locker.lockfile_name)
        fcntl.flock(self.file_pointer.fileno(), fcntl.LOCK_EX)

    def __exit__(self, _type, value, traceback):
        fcntl.flock(self.file_pointer.fileno(), fcntl.LOCK_UN)
        self.file_pointer.close()
