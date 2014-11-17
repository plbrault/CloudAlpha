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

class AuthenticationFailedAccountError(AccountError):
    pass


class ManagerError(Exception):
    pass

class ArgumentParsingManagerError(ManagerError):
    pass

class MissingAttributeManagerError(ManagerError):
    pass

class StartupFailedManagerError(ManagerError):
    pass
