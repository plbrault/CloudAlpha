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

"""This module defines custom exceptions for managers and services."""

class FileSystemError(Exception):
    pass

class InvalidPathFileSystemError(FileSystemError):
    pass

class InvalidTargetFileSystemError(FileSystemError):
    pass

class AlreadyExistsFileSystemError(FileSystemError):
    pass

class IDNotFoundFileSystemError(FileSystemError):
    pass

class InsufficientSpaceFileSystemError(FileSystemError):
    pass

class AccessFailedFileSystemError(FileSystemError):
    pass

class ForbiddenOperationFileSystemError(FileSystemError):
    pass


class AccountError(Exception):
    pass

class ArgumentParsingAccountError(AccountError):
    pass

class MissingAttributeAccountError(AccountError):
    pass

class MissingSettingAccountError(AccountError):
    pass

class AuthenticationFailedAccountError(AccountError):
    pass


class ManagerError(Exception):
    pass

class ArgumentParsingManagerError(ManagerError):
    pass

class MissingAttributeManagerError(ManagerError):
    pass

class MissingSettingManagerError(ManagerError):
    pass

class StartupFailedManagerError(ManagerError):
    pass


class SettingError(Exception):
    pass

class InvalidNameSettingError(SettingError):
    pass

class ValueParsingSettingError(SettingError):
    pass
