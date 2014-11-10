from core.exceptions import InvalidPathFileSystemError, InvalidTargetFileSystemError

class FileSystemView(object):

    _file_system = None
    _working_dir = "/"

    def get_abs_path(self, path):
        """Return the absolute path corresponding to the given relative path.
        """
        abs_levels = []
        if path[:1] == "/":
            path = path[1:]
        elif self._working_dir != "/":
            for level in self._working_dir[1:].split("/"):
                abs_levels.append(level)
        for level in path.split("/"):
            if level == "..":
                if len(abs_levels) > 0:
                    abs_levels.pop()
            elif level != ".":
                abs_levels.append(level)
        abs_path = ""
        for level in abs_levels:
            abs_path += "/" + level
        if abs_path == "":
            abs_path = "/"
        return abs_path

    @property
    def working_dir(self):
        """Return the path of the current working directory.
        
        The return value is a POSIX pathname, with "/" representing the root of the file system.
        """
        return self._working_dir

    @working_dir.setter
    def working_dir(self, path):
        """Change the working directory.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the given path does not correspond to a directory, raise InvalidTargetFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        with self._file_system.lock:
            abs_path = self.get_abs_path(path)
            if not self._file_system.exists(abs_path):
                raise InvalidPathFileSystemError()
            if not self._file_system.is_dir(abs_path):
                raise InvalidTargetFileSystemError()
            self._working_dir = abs_path

    @property
    def space_used(self):
        """Return the number of bytes used on the file system.
        
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        return self._file_system.space_used

    @property
    def free_space(self):
        """Return the free space remaining on the file system, in bytes.
        
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        return self._file_system.free_space

    def exists(self, path):
        """Return True if the given path points to an existing file or directory, excluding uncommitted files.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the real file system is inaccessible, raise AccessFailedFileSystemError.        
        """
        abs_path = self.get_abs_path(path)
        return self._file_system.exists(abs_path)

    def list_dir(self, path=None):
        """Return the content of the specified directory. If no directory is specified, return the content of the current working directory.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
                
        The return value is a list of file and folder names. It does not contain references to the current
        or parent directory (e.g. « . » or « .. »).
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the given path does not correspond to a directory, raise InvalidTargetFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        if path == None:
            abs_path = self._working_dir
        else:
            abs_path = self.get_abs_path(path)
        return self._file_system.list_dir(abs_path)

    def is_dir(self, path):
        """Return a boolean value indicating if the given path corresponds to a directory.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        abs_path = self.get_abs_path(path)
        return self._file_system.is_dir(abs_path)

    def is_file(self, path):
        """Return a boolean value indicating if the given path corresponds to a file.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        abs_path = self.get_abs_path(path)
        return self._file_system.is_file(abs_path)

    def get_size(self, path):
        """Return the size, in bytes, of the file corresponding to the given path.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the given path corresponds to a directory, raise FileSystemTargetError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError. 
        """
        abs_path = self.get_abs_path(path)
        return self._file_system.get_size(abs_path)

    def get_metadata(self, path=None):
        """Return a FileMetadata object representing the file or directory corresponding to the given path.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        If path is None, use the current working directory.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError. 
        """
        if path == None:
            abs_path = self._working_dir
        else:
            abs_path = self.get_abs_path(path)
        return self._file_system.get_metadata(abs_path)

    def get_content_metadata(self, path=None):
        """Return an iterable of FileMetadata objects representing the contents of the directory corresponding to the given path.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the given path does not point to a directory, raise InvalidTargetFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.         
        """
        if path == None:
            abs_path = self._working_dir
        else:
            abs_path = self.get_abs_path(path)
        return self._file_system.get_content_metadata(abs_path)

    def get_created_datetime(self, path):
        """Return the date and time of creation of the file or directory corresponding to the given path.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        The return value is a datetime object.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        abs_path = self.get_abs_path(path)
        return self._file_system.get_created_datetime(abs_path)

    def get_modified_datetime(self, path):
        """Return the date and time of the last modification to the file or directory corresponding to the given path.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        The return value is a datetime object.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        abs_path = self.get_abs_path(path)
        return self._file_system.get_modified_datetime(abs_path)

    def get_accessed_datetime(self, path):
        """Return the date and time of the last time the given file or directory was accessed.
        If not available, return the date and time of the last modification.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        The return value is a datetime object.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        abs_path = self.get_abs_path(path)
        return self._file_system.get_accessed_datetime(abs_path)

    def make_dir(self, path):
        """Creates a new directory corresponding to the given path.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the parent path is invalid, raise InvalidPathFileSystemError.
        If the given path corresponds to an existing file or directory, raise AlreadyExistsFileSystemError.
        If the given path corresponds to an uncommitted file or directory, raise UncommittedExistsFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        abs_path = self.get_abs_path(path)
        self._file_system.make_dir(abs_path)

    def move(self, old_path, new_path):
        """Move and/or rename a file or directory from old_path to new_path.
        
        new_path includes the new name of the file or directory.
        
        The paths must be POSIX pathnames, with "/" representing the root of the file system.
        They may be absolute, or relative to the current working directory.
        
        If old_path is invalid, raise InvalidPathFileSystemError.
        If new_path corresponds to an existing file or directory, raise AlreadyExistsFileSystemError.
        If new_path is a subpath of old_path , raise ForbiddenOperationFileSystemError.
        If new_path corresponds to an uncommitted file or directory, raise UncommittedExistsFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        abs_old_path = self.get_abs_path(old_path)
        abs_new_path = self.get_abs_path(new_path)
        self._file_system.move(abs_old_path, abs_new_path)

    def copy(self, path, copy_path):
        """Copy a file or directory from path to copy_path.
        
        new_path includes the name of the copied file or directory.
        The paths must be POSIX pathnames, with "/" representing the root of the file system.
        They may be absolute, or relative to the current working directory.
        
        If path is invalid, raise InvalidPathFileSystemError.
        If copy_path corresponds to an existing file or directory, raise AlreadyExistsFileSystemError.
        If new_path is a subpath of old_path , raise ForbiddenOperationFileSystemError.
        If copy_path corresponds to an uncommitted file or directory, raise UncommittedExistsFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError. 
        """
        abs_path = self.get_abs_path(path)
        abs_copy_path = self.get_abs_path(copy_path)
        self._file_system.copy(abs_path, abs_copy_path)

    def delete(self, path):
        """Delete the file or directory corresponding to the given path.
        
        If the given path corresponds to a directory that is not empty, all its files and subdirectories
        must be deleted first.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        abs_path = self.get_abs_path(path)
        self._file_system.delete(abs_path)

    def read(self, path, start_byte, num_bytes=None):
        """Read the number of bytes corresponding to num_bytes from the file corresponding to the given path,
        beginning at start_byte.
        
        If start_byte is greater than the size of the file, return an empty iterable.
        
        If num_bytes is not specified, read all remaining bytes of the file.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        The return value is an iterable of bytes.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the given path corresponds to a directory, raise InvalidTargetFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        abs_path = self.get_abs_path(path)
        return self._file_system.read(abs_path, start_byte, num_bytes)

    def create_new_file(self, caller_unique_id, path):
        """Create an empty file corresponding to the given path.
        
        If a file corresponding to this path already exists, it is overwritten.
        
        The caller_unique_id is used to ensure that only the file creator can write to it, flush it or commit it.
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        The size parameter indicates the number of bytes that must be allocated for the new file.
        
        If the parent path is invalid, raise InvalidPathFileSystemError.
        If the given path corresponds to an existing directory, raise InvalidTargetFileSystemError.
        If the given path corresponds to an uncommitted file or directory, raise UncommittedExistsFileSystemError.        
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        abs_path = self.get_abs_path(path)
        self._file_system.create_new_file(caller_unique_id, abs_path)

    def write_to_new_file(self, caller_unique_id, path, data):
        """Append the given data to the uncommitted file corresponding to the given path.
        
        The caller_unique_id is used to ensure that only the file creator can write to it.
        The data must be an iterable of bytes.
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path does not correspond to an uncommitted file, raise InvalidTargetFileSystemError.
        If caller_unique_id does not correspond to the unique_id of the file creator, raise ForbiddenOperationFileSystemError.
        If there is not enough free space to store the new data, raise InsufficientSpaceFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        abs_path = self.get_abs_path(path)
        self._file_system.write_to_new_file(caller_unique_id, abs_path, data)

    def commit_new_file(self, caller_unique_id, path):
        """Commit a file that was previously created/overwritten, then populated with data.
        
        The caller_unique_id is used to ensure that only the file creator can commit it.
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.        
        
        If the given path does not correspond to an uncommitted file, raise InvalidTargetFileSystemError.
        If caller_unique_id does not correspond to the unique_id of the file creator, raise ForbiddenOperationFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        abs_path = self.get_abs_path(path)
        self._file_system.commit_new_file(caller_unique_id, abs_path)

    def flush_new_file(self, caller_unique_id, path):
        """Delete an uncommitted file.
        
        The caller_unique_id is used to ensure that only the file creator can flush it.
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path does not correspond to an uncommitted file, raise InvalidTargetFileSystemError.
        If caller_unique_id does not correspond to the unique_id of the file creator, raise ForbiddenOperationFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.                
        """
        abs_path = self.get_abs_path(path)
        self._file_system.flush_new_file(abs_path)

    def new_file_exists(self, path):
        """Return True if the given path corresponds to an uncommitted file.
        
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        abs_path = self.get_abs_path(path)
        return self._file_system.new_file_exists(abs_path)

    def __init__(self, file_system):
        """Create a new FileSystemView instance linked to the given FileSystem subclass instance."""
        self._file_system = file_system
