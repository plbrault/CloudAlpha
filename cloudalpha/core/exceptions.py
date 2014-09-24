class FileSystemError(Exception):
    pass
        
class InvalidPathFileSystemError(FileSystemError):
    pass

class InvalidTargetFileSystemError(FileSystemError):
    pass

class AlreadyExistsFileSystemError(FileSystemError):
    pass