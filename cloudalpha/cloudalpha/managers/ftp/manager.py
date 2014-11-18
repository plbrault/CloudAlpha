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

from cloudalpha.manager import Manager
from cloudalpha.managers.ftp.ftp_server.ftp_server import FTPServer
from cloudalpha.exceptions import MissingAttributeManagerError, ArgumentParsingManagerError

class FTPManager(Manager):
    """This manager allows the interaction with a file storage account through the FTP protocol."""

    unique_id = None
    file_system_view = None
    server_port = None
    ftp_username = None
    ftp_password = None

    _server = None

    def run(self):
        """Put the manager into action.
        
        If a required attribute is not set, raise MissingAttributeManagerError.
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
        """Initialize the manager with the given parameters.
        
        server_port argument accepts a string value, but it must be convertible to an integer.
        
        If server_port is a string that cannot be parsed to an integer, raise ArgumentParsingManagerError.
        """
        if server_port:
            try:
                server_port = int(server_port)
            except:
                raise ArgumentParsingManagerError
        self.unique_id = unique_id
        self.file_system_view = file_system_view
        self.server_port = server_port
        self.ftp_username = ftp_username
        self.ftp_password = ftp_password
