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

from abc import ABCMeta, abstractmethod

class Settings:
    """A base class for implementing global settings in services and managers."""

    __metaclass__ = ABCMeta

    @classmethod
    @abstractmethod
    def set(cls, name, value):
        """Update the value of the setting corresponding to name.
        
        If there is no setting corresponding to name, raise InvalidNameSettingError.
        
        value can be of type string. It will be converted to the proper type before 
        it is stored. In case of parsing failure, raise ValueParsingSettingError.
        """
