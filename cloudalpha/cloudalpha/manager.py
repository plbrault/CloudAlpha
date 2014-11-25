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

class Manager(object):

    """A base class for implementing a file manager accessible through a specific
    interface, as a network protocol.
    
    Upon its initialization, an instance of a Manager subclass is provided with
    an instance of a FileSystemView subclass, which it is intended to interact with.
    """

    __metaclass__ = ABCMeta

    unique_id = None
    file_system_view = None

    @abstractmethod
    def run(self):
        """Put the manager into action, in a new thread. If already done, do nothing.
        
        If a required instance attribute is not set, raise MissingAttributeManagerError.
        If a required setting is not set, raise MissingSettingManagerError.
        If the operation fails for any other reason, raise StartupFailedManagerError.
        """
        pass

    @abstractmethod
    def stop(self):
        """Stop the manager.
        
        If the manager is already stopped, do nothing.
        """
        pass

    def __init__(self, unique_id, file_system_view=None, *args, **kwargs):
        """The super initializer for Manager subclasses.
        
        Subclass initializers must take the same first 3 arguments, 
        and all subsequent arguments must be optional and must accept 
        string values.
        
        If an argument cannot be parsed to the proper type,
        raise ArgumentParsingManagerError.
        """
        self.unique_id = unique_id
        self.file_system_view = file_system_view
