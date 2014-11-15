from pyftpdlib.handlers import DTPHandler

class AdaptedDTPHandler(DTPHandler):

    file_path = None
    _new_file_id = None

    class FileAdapter(object):

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

    _file_adapter = None

    @property
    def file_obj(self):
        if self.file_path is None:
            return None
        else:
            return self.FileAdapter(self.cmd_channel.fs.file_system_view, self.file_path, self._new_file_id)

    @file_obj.setter
    def file_obj(self, obj):
        pass

    def __init__(self, sock, cmd_channel):
        super(AdaptedDTPHandler, self).__init__(sock, cmd_channel)

    def _posix_ascii_data_wrapper(self, chunk):
        return chunk

    def enable_receiving(self, type, cmd):
        self.file_path = self.cmd_channel.upload_path
        file_system_view = self.cmd_channel.fs.file_system_view
        self._new_file_id = file_system_view.create_new_file()
        super(AdaptedDTPHandler, self).enable_receiving(type, cmd)

    def close(self):
        if not self._closed and self.file_obj != None:
            file_system_view = self.cmd_channel.fs.file_system_view
            if self.transfer_finished:
                file_system_view.commit_new_file(self._new_file_id, self.file_path)
            else:
                file_system_view.flush_new_file(self._new_file_id)
        self.cmd_channel._on_dtp_close()
        super(AdaptedDTPHandler, self).close()