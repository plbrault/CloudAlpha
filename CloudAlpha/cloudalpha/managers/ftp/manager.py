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
from cloudalpha.managers.ftp.settings import FTPSettings
from cloudalpha.exceptions import MissingAttributeManagerError, StartupFailedManagerError, MissingSettingManagerError

class FTPManager(Manager):
    """This manager allows the interaction with a file storage account through the FTP protocol."""

    unique_id = None
    file_system_view = None
    ftp_username = None
    ftp_password = None

    _running = False

    def run(self):
        """Put the manager into action in a new thread. If already done, do nothing.
        
        If a required instance attribute is not set, raise MissingAttributeManagerError.
        If a required setting is not set, raise MissingSettingManagerError.
        If the operation fails for any other reason, raise StartupFailedManagerError.
        """
        if not self._running:
            if FTPServer().user_exists(self.ftp_username):
                raise StartupFailedManagerError("Username " + self.ftp_username + " already exists")
            if self.file_system_view is None or self.ftp_username is None or self.ftp_password is None:
                raise MissingAttributeManagerError
            if not FTPSettings.ftp_server_port:
                raise MissingSettingManagerError
            FTPServer().add_user(self.ftp_username, self.ftp_password, self.file_system_view)
            FTPServer().start_using()

    def stop(self):
        """Stop the manager.
        
        If the manager is already stopped, do nothing.
        """
        if self._started:
            FTPServer().remove_user(self.ftp_username)
            FTPServer().stop_using()
            print("""FTP Manager "%0s" stopped.""" % (self.unique_id))
        else:
            print("""FTP Manager "%0s" already stopped.""" % (self.unique_id))

    def __init__(self, unique_id, file_system_view=None, ftp_username=None, ftp_password=None):
        """Initialize the manager with the given parameters."""
        self.unique_id = unique_id
        self.file_system_view = file_system_view
        self.ftp_username = ftp_username
        self.ftp_password = ftp_password
