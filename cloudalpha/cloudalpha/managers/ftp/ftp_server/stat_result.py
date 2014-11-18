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

class StatResult():
    """A mock of the os.stat result class."""

    st_mode = None
    st_ino = 0
    st_dev = 0
    st_nlink = 1
    st_uid = 0
    st_gid = 0
    st_size = None
    st_atime = None
    st_mtime = None
    st_ctime = None

    def __init__(self, mode, size, accessed_time, modified_time, created_time):
        """StatResult initializer"""
        self.st_mode = mode
        self.st_size = size
        self.st_atime = accessed_time
        self.st_mtime = modified_time
        self.st_ctime = created_time

    class Modes:
        """Enumeration of st_mode possible values."""
        FILE = 33206
        DIRECTORY = 16895
