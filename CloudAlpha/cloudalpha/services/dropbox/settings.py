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

from cloudalpha.settings import Settings
from cloudalpha.exceptions import InvalidNameSettingError

class DropboxSettings(Settings):
    """This class contains global settings accessible by all Dropbox accounts."""

    app_key = None
    app_secret = None

    @classmethod
    def set(cls, name, value):
        """Update the value of the setting corresponding to name.
        
        If there is no setting corresponding to name, raise InvalidNameSettingError.
        
        value can be of type string. It will be converted to the proper type before 
        it is stored. In case of parsing failure, raise ValueParsingSettingError.
        """
        if name == "app_key":
            cls.app_key = str(value)
        elif name == "app_secret":
            cls.app_secret = str(value)
        else:
            raise InvalidNameSettingError