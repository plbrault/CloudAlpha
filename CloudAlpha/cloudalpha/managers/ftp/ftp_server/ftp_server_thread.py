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

from threading import Thread

class FTPServerThread(Thread):
    """A thread for running a FTPServer instance."""

    ftp_server = None

    def __init__(self, ftp_server):
        """FTPServerThread initializer"""
        self.ftp_server = ftp_server
        super(FTPServerThread, self).__init__()

    def run(self):
        """Start the thread and the FTP server."""
        self.ftp_server.serve_forever()
