# =============================================================================
# Copyright (C) 2014 Pier-Luc Brault and Alex Cline
#
# This file is part of CloudAlpha.
#
# CloudAlpha is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CloudAlpha is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with CloudAlpha.  If not, see <http://www.gnu.org/licenses/>.
#
# http://github.com/plbrault/cloudalpha
# =============================================================================

from pyftpdlib.servers import FTPServer as Server
from pyftpdlib.authorizers import DummyAuthorizer
from cloudalpha.managers.ftp import settings
from cloudalpha.managers.ftp.ftp_server.ftp_server_thread import FTPServerThread
import cloudalpha.managers.ftp.ftp_server.strerror  # @UnusedImport

class FTPServer:
    """A singleton FTP server which each user has access to a distinct 
    cloudalpha.file_system_view.FileSystemView instance.
    """

    _instance = None

    _port = None
    _server = None
    _thread = None
    _authorizer = DummyAuthorizer()
    _file_system_views = {}

    use_count = 0

    def __new__(cls, *args, **kwargs):
        """Return the singleton instance."""
        if not cls._instance:
            cls._instance = super(FTPServer, cls).__new__(cls, *args, **kwargs)
            cls._instance._port = settings.ftp_server_port
        return cls._instance

    def user_exists(self, username):
        """Return a boolean value indicating if the specified username exists."""
        return username in self._file_system_views

    def add_user(self, username, password, file_system_view):
        """Add a new user with the given username and password, associated
        to the specified cloudalpha.file_system_view.FileSystemView instance."""
        self._file_system_views[username] = file_system_view
        self._authorizer.add_user(username, password, "/", perm="elradfmw")

    def remove_user(self, username):
        """Remove the user corresponding to the given username."""
        self._authorizer.remove_user(username)
        del self._file_system_views[username]

    def get_file_system_view(self, username):
        """Get the cloudalpha.file_system_view.FileSystemView instance
        corresponding to the given username."""
        return self._file_system_views[username]

    def start_using(self):
        """Increment use_count. If the FTP server is currently not running, start it in a new thread."""
        self.use_count += 1
        if self._server is None:
            from cloudalpha.managers.ftp.ftp_server.file_system_adapter import FileSystemAdapter
            from cloudalpha.managers.ftp.ftp_server.adapted_ftp_handler import AdaptedFTPHandler

            # Get FileSystemAdapter
            fs_adapter = FileSystemAdapter

            # Initiate the FTP Handler class
            handler = AdaptedFTPHandler
            handler.authorizer = self._authorizer
            handler.abstracted_fs = fs_adapter
            handler.banner = "CloudAlpha FTP manager ready."

            # Initiate and start the server
            self._server = Server(("0.0.0.0", self._port), handler)
            self._server.max_cons = self._server.max_cons_per_ip = 256
            self._thread = FTPServerThread(self._server)
            self._thread.start()

    def stop_using(self):
        """If the FTP server is currently running, decrement use_count. If
        the new value of use_count is zero, stop the server."""
        if self._server is not None:
            self.use_count -= 1
            if self.use_count < 1:
                self._server.stop()
                return True
