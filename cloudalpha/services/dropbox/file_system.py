from core.file_system import FileSystem
from dropbox.client import DropboxClient
from core.exceptions import InvalidPathFileSystemError, InvalidTargetFileSystemError, AccessFailedFileSystemError
from threading import RLock

import os
import json

class DropBoxFileSystem(FileSystem):

    _lock = RLock()
    _working_dir = '/'

    def list_dir(self, path):
        """Return the content of the specified directory. If no directory is specified, return the content of the current working directory.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
                
        The return value is a list of file and folder names. It does not contain references to the current
        or parent directory (e.g. « . » or « .. »).
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the given path does not correspond to a directory, raise InvalidTargetFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        items = ""
        with self._lock:
            if not os.path.exists(path):
                raise InvalidPathFileSystemError()
            if not os.path.isdir(path):
                raise InvalidTargetFileSystemError()
            try:
                dropbox_meta = self._client.metadata(path)
                for contents in dropbox_meta["contents"]:
                    items = items + " " + contents['path']
                return items
            except:
                raise AccessFailedFileSystemError()


    def __init__(self, account):
        super(DropBoxFileSystem, self).__init__(account)
