"""TODO: 

Implement a dummy file system, for testing purposes.

Reminder: Account and FileSystem subclasses must be implemented in a thread-safe way.
"""

from core.file_system import FileSystem
from core.exceptions import InvalidPathFileSystemError, AlreadyExistsFileSystemError, InvalidTargetFileSystemError
from core.exceptions import AccessFailedFileSystemError
import os, time, shutil

class DummyFileSystem(FileSystem):

    _real_root_dir = "temp"
    _total_space = 1000000000
    _space_used = 0

    def _get_absolute_virtual_path(self, path):
        """Return the absolute virtual path corresponding to the given relative one.
        """
        if path[:1] == "/":
            return path
        else:
            abs_levels = [self._working_dir]
            for level in path.split("/"):
                if level == ".." and len(abs_levels) > 0:
                    abs_levels.pop()
                elif level != ".":
                    abs_levels.append(level)
            abs_path = ""
            for level in abs_levels:
                abs_path += "/" + level
            return abs_path

    def _get_real_path(self, path):
        """Return the real path corresponding to the specified virtual path.
        """
        path = self._get_absolute_virtual_path(path)
        return os.path.abspath(os.path.join(self._real_root_dir, path[1:]))

    @property
    def working_dir(self):
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
        real_path = self._get_real_path(path)
        if not os.path.exists(real_path):
            raise InvalidPathFileSystemError()
        if not os.path.isdir(self._get_real_path(path)):
            raise InvalidTargetFileSystemError()
        self._working_dir = path

    @property
    def space_used(self):
        """Return the number of bytes used on the file system.
        
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        return self._space_used

    @property
    def free_space(self):
        """Return the free space remaining on the file system, in bytes.
        
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        return self._total_space - self._space_used

    def exists(self, path):
        """Return True if the given path is valid.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the real file system is inaccessible, raise AccessFailedFileSystemError.        
        """
        return os.path.exists(self._get_real_path(path))

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
        if path is None:
            path = self._get_real_path(self._working_dir)
            return os.listdir(path)
        else:
            path = self._get_real_path(path)
            if not os.path.exists(path):
                raise InvalidPathFileSystemError()
            if not os.path.isdir(path):
                raise InvalidTargetFileSystemError()
            try:
                return os.listdir(path)
            except:
                raise AccessFailedFileSystemError()


    def is_dir(self, path):
        """Return a boolean value indicating if the given path corresponds to a directory.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        path = self._get_real_path(path)
        if not os.path.exists(path):
            raise InvalidPathFileSystemError
        return os.path.isdir(path)

    def is_file(self, path):
        """Return a boolean value indicating if the given path corresponds to a file.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        path = self._get_real_path(path)
        if not os.path.exists(path):
            raise InvalidPathFileSystemError
        return os.path.isfile(path)

    def get_size(self, path):
        """Return the size, in bytes, of the file corresponding to the given path.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the given path corresponds to a directory, raise FileSystemTargetError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError. 
        """
        path = self._get_real_path(path)
        if not os.path.exists(path):
            raise InvalidPathFileSystemError()
        if os.path.isdir():
            raise InvalidTargetFileSystemError()
        try:
            return os.path.getsize(path)
        except:
            raise AccessFailedFileSystemError()

    def get_created_datetime(self, path):
        """Return the date and time of creation of the file or directory corresponding to the given path.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        The return value is a datetime object.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        path = self._get_real_path(path)
        if not os.path.exists(path):
            raise InvalidPathFileSystemError
        try:
            return time.ctime(os.path.getctime(path))
        except:
            raise AccessFailedFileSystemError()

    def get_modified_datetime(self, path):
        """Return the date and time of the last modification to the file or directory corresponding to the given path.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        The return value is a datetime object.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        path = self._get_real_path(path)
        if not os.path.exists(path):
            raise InvalidPathFileSystemError
        try:
            return time.ctime(os.path.getmtime(path))
        except:
            raise AccessFailedFileSystemError()

    def get_accessed_datetime(self, path):
        """Return the date and time of the last time the given file or directory was accessed.
        If not available, return the date and time of the last modification.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        The return value is a datetime object.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        path = self._get_real_path(path)
        if not os.path.exists(path):
            raise InvalidPathFileSystemError
        try:
            return time.ctime(os.path.getatime(path))
        except:
            raise AccessFailedFileSystemError()

    def make_dir(self, path):
        """Creates a new directory corresponding to the given path.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the parent path is invalid, raise InvalidPathFileSystemError.
        If the given path corresponds to an existing file or directory, raise AlreadyExistsFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        path = self._get_real_path(path)
        if not os.path.exists(path.rsplit("/", 1)[0]):
            raise InvalidPathFileSystemError()
        if os.path.exists(path):
            raise AlreadyExistsFileSystemError()
        try:
            os.mkdir(path)
        except:
            raise AccessFailedFileSystemError()

    def move(self, old_path, new_path):
        """Move and/or rename a file or directory from old_path to new_path.
        
        new_path includes the new name of the file or directory.
        
        The paths must be POSIX pathnames, with "/" representing the root of the file system.
        They may be absolute, or relative to the current working directory.
        
        If at least one of the given paths is invalid, raise InvalidPathFileSystemError.
        If new_path corresponds to an existing file or directory, raise AlreadyExistsFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        old_path = self._get_real_path(old_path)
        new_path = self._get_real_path(new_path)
        if not os.path.exists(old_path):
            raise InvalidPathFileSystemError()
        if old_path in new_path:
            raise InvalidPathFileSystemError()
        if os.path.exists(new_path):
            raise AlreadyExistsFileSystemError()
        try:
            shutil.move(old_path, new_path)
        except:
            raise AccessFailedFileSystemError()

    def copy(self, path, copy_path):
        """Copy a file or directory from path to copy_path.
        
        new_path includes the name of the copied file or directory.
        The paths must be POSIX pathnames, with "/" representing the root of the file system.
        They may be absolute, or relative to the current working directory.
        
        If at least one of the given paths is invalid, raise InvalidPathFileSystemError.
        If copy_path corresponds to an existing file or directory, raise AlreadyExistsFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError. 
        """
        path = self._get_real_path(path)
        copy_path = self._get_real_path(copy_path)
        if not os.path.exists(path):
            raise InvalidPathFileSystemError()
        if path in copy_path:
            raise InvalidPathFileSystemError()
        if os.path.exists(copy_path):
            raise AlreadyExistsFileSystemError()
        try:
            shutil.copy(path, copy_path)
        except:
            raise AccessFailedFileSystemError()

    def delete(self, path):
        """Delete the file or directory corresponding to the given path.
        
        If the given path corresponds to a directory that is not empty, all its files and subdirectories
        must be deleted first.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        path = self._get_real_path(path)
        if os.path.exists(path):
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
            except:
                raise AccessFailedFileSystemError()
        else:
            raise InvalidPathFileSystemError()

    def read(self, path, start_byte, num_bytes):
        """Read the number of bytes corresponding to num_bytes from the file corresponding to the given path,
        beginning at start_byte.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        The return value is an iterable of bytes.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the given path corresponds to a directory, raise InvalidTargetFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        path = self._get_real_path(path)
        if not os.path.exists(path):
            raise InvalidPathFileSystemError()
        if os.path.isdir():
            raise InvalidTargetFileSystemError()
        try:
            file = open(path, 'rb')
            file.seek(start_byte)
            data = bytearray(file.read(num_bytes))
            file.close()
            return data
        except:
            raise AccessFailedFileSystemError()

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
        path = self._get_real_path(path)
        if not os.path.isfile(path):
            open(path, "a").close()

            self._total_space = self._total_space - size
            self._space_used = self._space_used + size


    def write_to_new_file(self, path, data):
        """Append the given data to the uncommitted file corresponding to the given path.
        
        The data must be an iterable of bytes.
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the given path does not correspond to an uncommitted file, raise InvalidTargetFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        path = self._get_real_path(path)
        file = open(path, 'a')
        file.write(data)
        file.close()

    def commit_new_file(self, path):
        """Commit a file that was previously created/overwritten, then populated with data.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.        
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the given path is valid, but does not correspond to an uncommitted file, raise InvalidTargetFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass

    def __init__(self):
        super(DummyFileSystem, self).__init__()
        root = os.path.abspath(self._real_root_dir)
        if os.path.exists(root):
            if os.path.isdir(root):
                shutil.rmtree(root, True)
            else:
                os.remove(root)
        os.mkdir(root)
        self.working_dir = "/"
