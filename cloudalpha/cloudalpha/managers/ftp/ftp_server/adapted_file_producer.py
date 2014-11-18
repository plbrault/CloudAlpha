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
# This file contains work derived from the source code of the pyftpdlib library,
# covered by the following copyright notice:
#
# Copyright (C) 2007-2014 Giampaolo Rodola' <g.rodola@gmail.com>
#
# ==============================================================================

from pyftpdlib.handlers import FileProducer, _FileReadWriteError
from cloudalpha.exceptions import InvalidPathFileSystemError, AccessFailedFileSystemError

class AdaptedFileProducer(FileProducer):
    """This class handles the reading of data from a file on the file system."""

    _offset = 0
    file_system_view = None
    _file_path = None

    def __init__(self, file_system_view, file_path):
        """AdaptedFileProducer instance initializer"""
        self.file_system_view = file_system_view
        self._file_path = file_path

    def more(self):
        """Attempt a chunk of data of size self.buffer_size."""
        try:
            data = self.file_system_view.read(self._file_path, self._offset, self.buffer_size)
            self._offset += self.buffer_size
            return data
        except InvalidPathFileSystemError:
            raise _FileReadWriteError("No such file or directory")
        except AccessFailedFileSystemError:
            raise _FileReadWriteError("File system currently inaccessible")

