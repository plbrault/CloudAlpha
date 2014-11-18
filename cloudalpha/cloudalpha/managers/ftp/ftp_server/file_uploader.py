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

class FileUploader(object):
    """This class handles the writing to a file of the file system
    in order to store files transferred from the client to the server."""

    _file_path = None
    _new_file_id = None
    _file_system_view = None

    closed = False

    @property
    def name(self):
        """Return the path of the file."""
        return self._file_path

    def __init__(self, file_system_view, file_path, new_file_id):
        """FileUploader initializer"""
        self._file_system_view = file_system_view
        self._file_path = file_path
        self._new_file_id = new_file_id

    def write(self, chunk):
        """Append a chunk of data to the end of the file."""
        self._file_system_view.write_to_new_file(self._new_file_id, chunk)

    def close(self):
        """Set closed to True."""
        self.closed = True
