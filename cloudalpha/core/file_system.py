from abc import ABCMeta, abstractmethod
from core.file_system_view import FileSystemView

class FileSystem(object):

    """A base class for implementing an abstraction of a file system, that may in fact
    be an adapter for managing the content of a file hosting service account.
    
    A subclass of FileSystem is defined for each supported file hosting service.
    An instance of a FileSystem subclass is linked to a single
    instance of an Account subclass.
    
    Account and FileSystem subclasses must be implemented in a thread-safe way.
    """

    __metaclass__ = ABCMeta

    _account = None

    @property
    @abstractmethod
    def lock(self):
        """Return the Lock object for the current instance."""
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
    def exists(self, path):
        """Return True if the given path points to an existing file or directory, excluding uncommitted files.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If the real file system is inaccessible, raise AccessFailedFileSystemError.        
        """
        pass

    @abstractmethod
    def list_dir(self, path):
        """Return the content of the specified directory.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
                
        The return value is a list of file and folder names. It does not contain references to the current
        or parent directory (e.g. « . » or « .. »).
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the given path does not correspond to a directory, raise InvalidTargetFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass

    @abstractmethod
    def is_dir(self, path):
        """Return a boolean value indicating if the given path corresponds to a directory.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass

    @abstractmethod
    def is_file(self, path):
        """Return a boolean value indicating if the given path corresponds to a file.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass

    @abstractmethod
    def get_size(self, path):
        """Return the size, in bytes, of the file corresponding to the given path.
        If the path points to a directory, return 0.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError. 
        """
        pass

    @abstractmethod
    def get_metadata(self, path):
        """Return a FileMetadata object representing the file or directory corresponding to the given path.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError. 
        """
        pass

    @abstractmethod
    def get_content_metadata(self, path):
        """Return an iterable of FileMetadata objects representing the contents of the directory corresponding to the given path.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the given path does not point to a directory, raise InvalidTargetFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.         
        """
        pass

    @abstractmethod
    def get_created_datetime(self, path):
        """Return the date and time of creation of the file or directory corresponding to the given path.
        If not available, return the date and time of the last modification.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        The return value is a datetime object.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass

    @abstractmethod
    def get_modified_datetime(self, path):
        """Return the date and time of the last modification to the file or directory corresponding to the given path.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        The return value is a datetime object.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass

    @abstractmethod
    def get_accessed_datetime(self, path):
        """Return the date and time of the last time the given file or directory was accessed.
        If not available, return the date and time of the last modification.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        The return value is a datetime object.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass

    @abstractmethod
    def make_dir(self, path):
        """Creates a new directory corresponding to the given path.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If the parent path is invalid, raise InvalidPathFileSystemError.
        If the given path corresponds to an existing file or directory, raise AlreadyExistsFileSystemError.
        If the given path corresponds to an uncommitted file or directory, raise UncommittedExistsFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass

    @abstractmethod
    def move(self, old_path, new_path):
        """Move and/or rename a file or directory from old_path to new_path.
        
        new_path includes the new name of the file or directory.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If old_path is invalid, raise InvalidPathFileSystemError.
        If new_path corresponds to an existing file or directory, raise AlreadyExistsFileSystemError.
        If new_path is a subpath of old_path , raise ForbiddenOperationFileSystemError.
        If new_path corresponds to an uncommitted file or directory, raise UncommittedExistsFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass

    @abstractmethod
    def copy(self, path, copy_path):
        """Copy a file or directory from path to copy_path.
        
        new_path includes the name of the copied file or directory.
        The paths must be absolute POSIX pathnames, with "/" representing the root of the file system.
        
        If path is invalid, raise InvalidPathFileSystemError.
        If copy_path corresponds to an existing file or directory, raise AlreadyExistsFileSystemError.
        If new_path is a subpath of old_path , raise ForbiddenOperationFileSystemError.
        If copy_path corresponds to an uncommitted file or directory, raise UncommittedExistsFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError. 
        """
        pass

    @abstractmethod
    def delete(self, path):
        """Delete the file or directory corresponding to the given path.
        
        If the given path corresponds to a directory that is not empty, all its files and subdirectories
        must be deleted first.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass

    @abstractmethod
    def read(self, path, start_byte, num_bytes=None):
        """Read the number of bytes corresponding to num_bytes from the file corresponding to the given path,
        beginning at start_byte.
        
        If start_byte is greater than the size of the file, return an empty iterable.
        
        If num_bytes is not specified, read all remaining bytes of the file.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        The return value is an iterable of bytes.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the given path corresponds to a directory, raise InvalidTargetFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass

    @abstractmethod
    def create_new_file(self, caller_unique_id, path):
        """Create an empty file corresponding to the given path.
        
        If a file corresponding to this path already exists, it is overwritten.
        
        The caller_unique_id is used to ensure that only the file creator can write to it, flush it or commit it.
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        The size parameter indicates the number of bytes that must be allocated for the new file.
        
        If the parent path is invalid, raise InvalidPathFileSystemError.
        If the given path corresponds to an existing directory, raise InvalidTargetFileSystemError.
        If the given path corresponds to an uncommitted file or directory, raise UncommittedExistsFileSystemError.        
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass

    @abstractmethod
    def write_to_new_file(self, caller_unique_id, path, data):
        """Append the given data to the uncommitted file corresponding to the given path.
        
        The caller_unique_id is used to ensure that only the file creator can write to it.
        The data must be an iterable of bytes.
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If the given path does not correspond to an uncommitted file, raise InvalidTargetFileSystemError.
        If caller_unique_id does not correspond to the unique_id of the file creator, raise ForbiddenOperationFileSystemError.
        If there is not enough free space to store the new data, raise InsufficientSpaceFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass

    @abstractmethod
    def commit_new_file(self, caller_unique_id, path):
        """Commit a file that was previously created/overwritten, then populated with data.
        
        The caller_unique_id is used to ensure that only the file creator can commit it.
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.     
        
        If the given path does not correspond to an uncommitted file, raise InvalidTargetFileSystemError.
        If caller_unique_id does not correspond to the unique_id of the file creator, raise ForbiddenOperationFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass

    @abstractmethod
    def flush_new_file(self, caller_unique_id, path):
        """Delete an uncommitted file.
        
        The caller_unique_id is used to ensure that only the file creator can flush it.
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If the given path does not correspond to an uncommitted file, raise InvalidTargetFileSystemError.
        If caller_unique_id does not correspond to the unique_id of the file creator, raise ForbiddenOperationFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.                
        """
        pass

    @abstractmethod
    def new_file_exists(self, path):
        """Return True if the given path corresponds to an uncommitted file.
        
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass

    def get_new_view(self):
        """Return a new FileSystemView linked to the current FileSystem subclass instance."""
        return FileSystemView(self)

    def __init__(self, account):
        """The super initializer for FileSystem subclasses."""
        self._account = account
