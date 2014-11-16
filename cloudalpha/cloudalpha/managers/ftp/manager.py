from cloudalpha.managers.ftp.ftp_server.ftp_server import FTPServer
from cloudalpha.exceptions import MissingAttributeManagerError

class FTPManager(object):

    unique_id = None
    file_system_view = None
    server_port = None
    ftp_username = None
    ftp_password = None

    _server = None

    def run(self):
        """Put the manager into action.
        
        If file_system is not set, raise FileSystemNotSetManagerError.
        If the operation fails for any other reason, raise StartupFailedManagerError.
        """
        if self.file_system_view is None or self.server_port is None or self.ftp_username is None or self.ftp_password is None:
            raise MissingAttributeManagerError
        if self._server is None:
            self._server = FTPServer(self.file_system_view, self.server_port, self.ftp_username, self.ftp_password)
            self._server.start()
            print("""FTP Manager "%0s" started.""" % (self.unique_id))
        else:
            print("""FTP Manager "%0s" already started.""" % (self.unique_id))

    def stop(self):
        """Stop the manager.
        
        If the manager is already stopped, do nothing.
        """
        if self._server is not None:
            self._server.stop()
            self._server = None
            print("""FTP Manager "%0s" stopped.""" % (self.unique_id))
        else:
            print("""FTP Manager "%0s" already stopped.""" % (self.unique_id))

    def __init__(self, unique_id, file_system_view=None, server_port=None, ftp_username=None, ftp_password=None):
        """Initialize the manager with the given parameters."""
        self.unique_id = unique_id
        self.file_system_view = file_system_view
        self.server_port = server_port
        self.ftp_username = ftp_username
        self.ftp_password = ftp_password