from pyftpdlib.handlers import FileProducer, _FileReadWriteError
from cloudalpha.exceptions import InvalidPathFileSystemError, AccessFailedFileSystemError

class AdaptedFileProducer(FileProducer):
    """This class handles the reading of data from a file on the file system."""

    _offset = 0
    file_system_view = None
    _file_path = None

    def __init__(self, file_system_view, file_path):
        """AdaptedFileProducer instance initializer"""
        self.file_system_view = file_system_view
        self._file_path = file_path

    def more(self):
        """Attempt a chunk of data of size self.buffer_size."""
        try:
            data = self.file_system_view.read(self._file_path, self._offset, self.buffer_size)
            self._offset += self.buffer_size
            return data
        except InvalidPathFileSystemError:
            raise _FileReadWriteError("No such file or directory")
        except AccessFailedFileSystemError:
            raise _FileReadWriteError("File system currently inaccessible")

