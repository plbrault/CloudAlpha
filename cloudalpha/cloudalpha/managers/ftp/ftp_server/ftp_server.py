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
from cloudalpha.managers.ftp.ftp_server.file_system_adapter import FileSystemAdapter
from cloudalpha.managers.ftp.ftp_server.adapted_ftp_handler import AdaptedFTPHandler
from cloudalpha.managers.ftp.ftp_server.ftp_server_thread import FTPServerThread
import cloudalpha.managers.ftp.ftp_server.strerror  # @UnusedImport

class FTPServer:
    """A FTP server with a single user account that has complete
    access to the supplied cloudalpha.file_system_view.FileSystemView instance.
    """

    file_system_view = None
    port = None
    username = None
    password = None

    _server = None
    _thread = None

    def __init__(self, file_system_view, port, username, password):
        """Init the FTP server with the given port, username and password."""
        self.file_system_view = file_system_view
        self.port = port
        self.username = username
        self.password = password

    def start(self):
        """Start the FTP server in a new thread."""
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
        """Stop the FTP server."""
        if self._server is not None:
            self._server.stop()
            return True
        else:
            return False
