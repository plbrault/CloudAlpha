class FileUploader(object):
    """This class handles the writing to a file of the file system
    in order to store files transferred from the client to the server."""

    _file_path = None
    _new_file_id = None
    _file_system_view = None

    closed = False

    @property
    def name(self):
        """Return the path of the file."""
        return self._file_path

    def __init__(self, file_system_view, file_path, new_file_id):
        """FileUploader initializer"""
        self._file_system_view = file_system_view
        self._file_path = file_path
        self._new_file_id = new_file_id

    def write(self, chunk):
        """Append a chunk of data to the end of the file."""
        self._file_system_view.write_to_new_file(self._new_file_id, chunk)

    def close(self):
        """Set closed to True."""
        self.closed = True
