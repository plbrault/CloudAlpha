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

class Account(object):
    """A base class for implementing an abstraction of a file hosting service account.
    
    A subclass is defined for each supported file hosting service.
    An instance of an Account subclass provides an instance of the FileSystem
    subclass corresponding to that service.
    """

    __metaclass__ = ABCMeta

    unique_id = None
    file_system = None

    @abstractmethod
    def authenticate(self):
        """Link the object to a real file hosting account. If already done, do nothing.
        
        The association process might require an interaction with the user.
        
        If a required instance attribute is not set, raise MissingAttributeAccountError.
        If a required setting is not set, raise MissingSettingAccountError.
        If the operation fails for any other reason, raise AuthenticationFailedAccountError.
        """

    def __init__(self, unique_id, *args, **kwargs):
        """The super initializer for Account subclasses.
        
        Subclass initializers must take the same first 2 arguments, 
        and all subsequent arguments must be optional and must accept 
        string values.
        
        If an argument cannot be parsed to the proper type,
        raise ArgumentParsingAccountError.
        """
        self.unique_id = unique_id

