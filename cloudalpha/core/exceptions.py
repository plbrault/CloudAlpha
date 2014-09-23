class FileSystemError(Exception):
    pass
        
class FileSystemInvalidPathError(FileSystemError):
    pass

class FileSystemInvalidTargetError(FileSystemError):
    pass