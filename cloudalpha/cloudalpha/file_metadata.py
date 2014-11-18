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

class FileMetadata(object):
    """Class representing the metadata of a file."""

    path = ""
    is_dir = False
    size = 0
    created_datetime = None
    accessed_datetime = None
    modified_datetime = None

    @property
    def name(self):
        """Return the short name of the file, excluding its location."""
        path = self.path
        if path[-1:] == "/":
            path = path[:-1]
        return path.rsplit("/", 1)[-1]

    def __init__(self, path="", is_dir=False, size=0, created_datetime=None, accessed_datetime=None, modified_datetime=None):
        """FileMetadata initializer"""
        self.path = path
        self.is_dir = is_dir
        self.size = size
        self.created_datetime = created_datetime
        self.accessed_datetime = accessed_datetime
        self.modified_datetime = modified_datetime

    def __str__(self):
        """Return a string representing the object."""
        return ('FileMetadata(path="' + self.path + '", name="' + self.name + '", is_dir=' + str(self.is_dir) + ", size=" + str(self.size)
            + ", created_datetime=" + str(self.created_datetime) + ", accessed_datetime=" + str(self.accessed_datetime)
            + ", modified_datetime=" + str(self.modified_datetime) + ")")
