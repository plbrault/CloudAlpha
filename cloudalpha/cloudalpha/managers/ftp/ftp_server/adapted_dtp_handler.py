# ==============================================================================
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
#
#
#
# This file contains work derived from the source code of the pyftpdlib library,
# covered by the following copyright notice:
# Copyright (C) 2007-2014 Giampaolo Rodola' <g.rodola@gmail.com>
#
# ==============================================================================

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
        """Shadow the file_obj attribute of the baseclass.
        If file_path is not set, return None. If file_path is
        set, return the corresponding FileUploader object.
        """
        if self.file_path is None:
            return None
        elif self._file_uploader is None:
            self._file_uploader = FileUploader(self.cmd_channel.fs.file_system_view, self.file_path, self._new_file_id)
        return self._file_uploader

    @file_obj.setter
    def file_obj(self, obj):
        """Dummy setter of the file_obj property, that shadows
        the file_obj attribute of the baseclass. It has no effect.
        """
        pass

    def __init__(self, sock, cmd_channel):
        """AdaptedDTPHandler initializer"""
        super(AdaptedDTPHandler, self).__init__(sock, cmd_channel)

    def _posix_ascii_data_wrapper(self, chunk):
        """Override the corresponding method of the baseclass.
        Return chunk as is.
        """
        return chunk

    def enable_receiving(self, type, cmd):
        """This method is called by the FTP handler to initialize
        the receiving of data from the client. 
        """
        self.file_path = self.cmd_channel.upload_path
        file_system_view = self.cmd_channel.fs.file_system_view
        self._new_file_id = file_system_view.create_new_file()
        super(AdaptedDTPHandler, self).enable_receiving(type, cmd)

    def close(self):
        """This method is called by the FTP handler when data
        transmission is finished.
        """
        if not self._closed and self.file_obj != None:
            file_system_view = self.cmd_channel.fs.file_system_view
            if self.transfer_finished:
                file_system_view.commit_new_file(self._new_file_id, self.file_path)
            else:
                file_system_view.flush_new_file(self._new_file_id)
            self._file_uploader = None
        self.cmd_channel._on_dtp_close()
        super(AdaptedDTPHandler, self).close()
