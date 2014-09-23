from abc import ABCMeta, abstractmethod

class FileSystem(object):
    __metaclass__ = ABCMeta
    
    @property
    @abstractmethod
    def cwd(self):
        """Return the path of the current working directory.
        
        The return value is a POSIX pathname, with "/" representing the root of the file system."""
        pass
    
    @cwd.setter
    @abstractmethod
    def cwd(self, path):
        """Change the working directory.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise FileSystemInvalidPathError.
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
        """
        pass
    
    @abstractmethod
    def is_dir(self, path):
        """Return a boolean value indicating if the given path represents a directory.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise InvalidPathError.
        """
        pass
    
    @abstractmethod
    def is_file(self, path):
        """Return a boolean value indicating if the given path represents a file.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise FileSystemInvalidPathError.
        """
        pass
    
    @abstractmethod
    def get_size(self, path):
        """Return the size, in bytes, of the file corresponding to the given path.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise FileSystemInvalidPathError.
        If the given path represents a directory, raise FileSystemTargetError.  
        """
        pass
    
    @abstractmethod
    def get_created_datetime(self, path):
        """Return the date and time of creation of the file or directory corresponding to the given path.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        The return value is a datetime object.
        
        If the given path is invalid, raise FileSystemInvalidPathError.
        """
        pass
    
    @abstractmethod
    def get_modified_datetime(self, path):
        """Return the date and time of the last modification to the file or directory corresponding to the given path.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        The return value is a datetime object.
        
        If the given path is invalid, raise FileSystemInvalidPathError.
        """
        pass
    
    @abstractmethod
    def get_accessed_datetime(self, path):
        """Return the date and time of the last time the given file or directory was accessed.
        If not available, return the date and time of the last modification.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        The return value is a datetime object.
        
        If the given path is invalid, raise FileSystemInvalidPathError.
        """
        pass        
    
    @abstractmethod
    def make_dir(self, path):
        """Creates a new directory corresponding to the given path.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the parent path is invalid, raise FileSystemInvalidPathError.
        """
        pass
    
    @abstractmethod
    def move(self, old_path, new_path):
        """Move and/or rename a file or directory from old_path to new_path.
        
        new_path includes the new name of the file or directory.
        
        The paths must be POSIX pathnames, with "/" representing the root of the file system.
        They may be absolute, or relative to the current working directory.
        
        If at least one of the given paths is invalid, raise FileSystemInvalidPathError. 
        """
        pass
    
    @abstractmethod
    def copy(self, path, copy_path):
        """Copy a file or directory from path to copy_path.
        
        new_path includes the name of the copied file or directory.
        The paths must be POSIX pathnames, with "/" representing the root of the file system.
        They may be absolute, or relative to the current working directory.
        
        If at least one of the given paths is invalid, raise FileSystemInvalidPathError.
        """
        pass
    
    @abstractmethod
    def delete(self, path):
        """Delete the file or directory corresponding to the given path.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise FileSystemInvalidPathError.
        """
        pass
    
    @abstractmethod
    def read(self, path, start_byte, end_byte):
        """Read the data from the given byte range of the file corresponding to the given path.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        The return value is an iterable of bytes.
        
        If the given path is invalid, raise FileSystemInvalidPathError.
        """
        pass
    
    @abstractmethod
    def put(self, path, data):
        """Append the given data to the unfinalized file corresponding to the given path.
        
        If the file does not exist, it is created.
        If the file exists and is finalized, it is overwritten.
        
        The data must be an iterable of bytes.
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise FileSystemInvalidPathError.
        """
        pass
    
    @abstractmethod
    def finalize(self, path):
        """Commit a file that was previously created/overwritten and populated with data.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.        
        
        If the given path is invalid, raise FileSystemInvalidPathError.
        If the given path does not represent an unfinalized file, raise FileSystemTargetError.
        """
        pass