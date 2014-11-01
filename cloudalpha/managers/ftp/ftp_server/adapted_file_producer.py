from pyftpdlib.handlers import FileProducer

class AdaptedFileProducer(FileProducer):

    _offset = 0
    file_system_view = None
    _file_path = None

    def __init__(self, file_system_view, file_path):
        """AdaptedFileProducer instance initializer"""
        self.file_system_view = file_system_view
        self._file_path = file_path

    def more(self):
        """Attempt a chunk of data of size self.buffer_size."""
        data = self.file_system_view.read(self._file_path, self._offset, self.buffer_size)
        self._offset += self.buffer_size
        return data
