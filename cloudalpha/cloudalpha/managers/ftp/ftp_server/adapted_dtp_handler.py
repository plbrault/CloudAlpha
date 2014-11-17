from pyftpdlib.handlers import DTPHandler
from cloudalpha.managers.ftp.ftp_server.file_uploader import FileUploader

class AdaptedDTPHandler(DTPHandler):
    """DTPHandler is the class handling data transfer between the server and the clients.
    AdaptedDTPHandler inherits from it to adapt the file upload process (from the FTP client
    to the server) to the use of cloudalpha.file_system.FileSystem subclasses. 
    """

    file_path = None
    _new_file_id = None
    _file_uploader = None

    @property
    def file_obj(self):
        if self.file_path is None:
            return None
        elif self._file_uploader is None:
            self._file_uploader = FileUploader(self.cmd_channel.fs.file_system_view, self.file_path, self._new_file_id)
        return self._file_uploader

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
            self._file_uploader = None
        self.cmd_channel._on_dtp_close()
        super(AdaptedDTPHandler, self).close()
