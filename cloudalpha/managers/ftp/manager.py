from core.exceptions import FileSystemNotSetManagerError
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.servers import FTPServer
from managers.ftp.ftp_server.file_system_adapter import FileSystemAdapter
from managers.ftp.ftp_server.adapted_ftp_handler import AdaptedFTPHandler

class FtpManager(object):

    unique_id = None
    file_system_view = None

    def run(self):
        """Put the manager into action.
        
        If file_system is not set, raise FileSystemNotSetManagerError.
        If the operation fails for any other reason, raise StartupFailedManagerError.
        """
        if self.file_system_view == None:
            raise FileSystemNotSetManagerError()

        # Generate FileSystemAdapter subclass
        fs_adapter = FileSystemAdapter.get_class(self.file_system_view)

        # Instantiate a dummy authorizer for managing 'virtual' users
        authorizer = DummyAuthorizer()

        # Define a new user having full r/w permissions
        authorizer.add_user('user', '12345', '.', perm='elradfmwM')

        # Instantiate FTP handler class
        handler = AdaptedFTPHandler
        handler.authorizer = authorizer
        handler.abstracted_fs = fs_adapter

        # Define a customized banner (string returned when client connects)
        handler.banner = "CloudAlpha FTP manager ready."

        # Instantiate FTP server class and listen on 127.0.0.1:2121
        address = ('127.0.0.1', 2121)
        server = FTPServer(address, handler)

        # set a limit for connections
        server.max_cons = 256
        server.max_cons_per_ip = 5

        # start ftp server
        server.serve_forever()

    def stop(self):
        """Stop the manager.
        
        If the manager is already stopped, do nothing.
        """
        pass

    def __init__(self, unique_id):
        """The super initializer for Manager subclasses."""
        self.unique_id = unique_id
