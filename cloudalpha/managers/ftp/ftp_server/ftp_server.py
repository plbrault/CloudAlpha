from pyftpdlib.servers import FTPServer as Server
from pyftpdlib.authorizers import DummyAuthorizer
from managers.ftp.ftp_server.file_system_adapter import FileSystemAdapter
from managers.ftp.ftp_server.adapted_ftp_handler import AdaptedFTPHandler
from managers.ftp.ftp_server.ftp_server_thread import FTPServerThread
import managers.ftp.ftp_server.strerror  # @UnusedImport

class FTPServer:

    file_system_view = None
    port = None
    username = None
    password = None

    _server = None
    _thread = None

    def __init__(self, file_system_view, port, username, password):
        self.file_system_view = file_system_view
        self.port = port
        self.username = username
        self.password = password

    def start(self):
        if self._server is None:
            # Generate FileSystemAdapter subclass
            fs_adapter = FileSystemAdapter.get_class(self.file_system_view)

            # Initiate the authorizer
            authorizer = DummyAuthorizer()
            authorizer.add_user(self.username, self.password, '.', perm='elradfmwM')

            # Initiate the FTP Handler
            handler = AdaptedFTPHandler
            handler.authorizer = authorizer
            handler.abstracted_fs = fs_adapter
            handler.banner = "CloudAlpha FTP manager ready."

            # Initiate and start the server
            self._server = Server(("localhost", self.port), handler)
            self._server.max_cons = self._server.max_cons_per_ip = 256
            self._thread = FTPServerThread(self._server)
            self._thread.start()

            return True
        else:
            return False

    def stop(self):
        if self._server is not None:
            self._server.stop()
            return True
        else:
            return False
