class FileUploader(object):

    _file_path = None
    _new_file_id = None
    _file_system_view = None

    closed = False

    @property
    def name(self):
        return self._file_path

    def __init__(self, file_system_view, file_path, new_file_id):
        self._file_system_view = file_system_view
        self._file_path = file_path
        self._new_file_id = new_file_id

    def write(self, chunk):
        self._file_system_view.write_to_new_file(self._new_file_id, chunk)

    def close(self):
        self.closed = True
