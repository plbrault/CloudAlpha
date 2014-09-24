class FileSystemError(Exception):
    pass
        
class InvalidPathFileSystemError(FileSystemError):
    pass

class InvalidTargetFileSystemError(FileSystemError):
    pass

class AlreadyExistsFileSystemError(FileSystemError):
    pass


class AccountError(Exception):
    pass

class ConnectionFailedAccountError(AccountError):
    pass


class ManagerError(Exception):
    pass

class FileSystemNotSetManagerError(ManagerError):
    pass

class StartupFailedManagerError(ManagerError):
    pass