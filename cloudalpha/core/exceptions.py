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

class AuthenticationFailedAccountError(AccountError):
    pass


class ManagerError(Exception):
    pass

class FileSystemNotSetManagerError(ManagerError):
    pass

class StartupFailedManagerError(ManagerError):
    pass
