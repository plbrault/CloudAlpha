from abc import ABCMeta, abstractmethod

class FileSystem(object):
    
    """A base class for implementing an abstraction of a file system, that may in fact
    be an adapter for managing the content of a file hosting service account.
    
    A subclass of FileSystem is defined for each supported file hosting service.
    An instance of a FileSystem subclass is linked to a single
    instance of an Account subclass.
    
    Account and FileSystem subclasses must be implemented in a thread-safe way.
    """
    
    __metaclass__ = ABCMeta
    
    @property
    @abstractmethod
    def cwd(self):
        """Return the path of the current working directory.
        
        The return value is a POSIX pathname, with "/" representing the root of the file system.
        """
        pass
    
    @cwd.setter
    @abstractmethod
    def cwd(self, path):
        """Change the working directory.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass    
    
    @property
    @abstractmethod
    def space_used(self):
        """Return the number of bytes used on the file system.
        
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass
    
    @property
    @abstractmethod
    def free_space(self):
        """Return the free space remaining on the file system, in bytes.
        
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass    
    
    @abstractmethod
    def list_dir(self, path=None):
        """Return the content of the specified directory. If no directory is specified, return the content of cwd.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
                
        The return value is a list of file and folder names. It does not contain references to the current
        or parent directory (e.g. « . » or « .. »).
        
        If the given path is invalid, raise InvalidPathError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass
    
    @abstractmethod
    def is_dir(self, path):
        """Return a boolean value indicating if the given path corresponds to a directory.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise InvalidPathError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass
    
    @abstractmethod
    def is_file(self, path):
        """Return a boolean value indicating if the given path corresponds to a file.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass
    
    @abstractmethod
    def get_size(self, path):
        """Return the size, in bytes, of the file corresponding to the given path.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the given path corresponds to a directory, raise FileSystemTargetError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError. 
        """
        pass
    
    @abstractmethod
    def get_created_datetime(self, path):
        """Return the date and time of creation of the file or directory corresponding to the given path.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        The return value is a datetime object.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass
    
    @abstractmethod
    def get_modified_datetime(self, path):
        """Return the date and time of the last modification to the file or directory corresponding to the given path.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        The return value is a datetime object.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass
    
    @abstractmethod
    def get_accessed_datetime(self, path):
        """Return the date and time of the last time the given file or directory was accessed.
        If not available, return the date and time of the last modification.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        The return value is a datetime object.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass        
    
    @abstractmethod
    def make_dir(self, path):
        """Creates a new directory corresponding to the given path.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the parent path is invalid, raise InvalidPathFileSystemError.
        If the given path corresponds to an existing file or directory, raise AlreadyExistsFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass
    
    @abstractmethod
    def move(self, old_path, new_path):
        """Move and/or rename a file or directory from old_path to new_path.
        
        new_path includes the new name of the file or directory.
        
        The paths must be POSIX pathnames, with "/" representing the root of the file system.
        They may be absolute, or relative to the current working directory.
        
        If at least one of the given paths is invalid, raise InvalidPathFileSystemError.
        If new_path corresponds to an existing file or directory, raise AlreadyExistsFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass
    
    @abstractmethod
    def copy(self, path, copy_path):
        """Copy a file or directory from path to copy_path.
        
        new_path includes the name of the copied file or directory.
        The paths must be POSIX pathnames, with "/" representing the root of the file system.
        They may be absolute, or relative to the current working directory.
        
        If at least one of the given paths is invalid, raise InvalidPathFileSystemError.
        If copy_path corresponds to an existing file or directory, raise AlreadyExistsFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError. 
        """
        pass
    
    @abstractmethod
    def delete(self, path):
        """Delete the file or directory corresponding to the given path.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass
    
    @abstractmethod
    def read(self, path, start_byte, end_byte):
        """Read the data from the given byte range of the file corresponding to the given path.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        The return value is an iterable of bytes.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the given path corresponds to a directory, raise InvalidTargetFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass
    
    @abstractmethod
    def create_new_file(self, path, size):
        """Create an empty file corresponding to the given path.
        
        If a file corresponding to this path already exists, it is overwritten.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        The size parameter indicates the number of bytes that must be allocated for the new file.
        
        If the parent path is invalid, raise InvalidPathFileSystemError.
        If the given path corresponds to an existing directory, raise InvalidTargetFileSystemError.
        If there is not enough free space to store the new file, raise InsufficientSpaceFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """        
        pass
    
    @abstractmethod
    def write_to_new_file(self, path, data):
        """Append the given data to the uncommitted file corresponding to the given path.
        
        The data must be an iterable of bytes.
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the given path does not correspond to an uncommitted file, raise InvalidTargetFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass
    
    @abstractmethod
    def commit_new_file(self, path):
        """Commit a file that was previously created/overwritten, then populated with data.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.        
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the given path is valid, but does not correspond to an uncommitted file, raise InvalidTargetFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass