"""TODO: 

Implement a dummy file system, for testing purposes.

Reminder: Account and FileSystem subclasses must be implemented in a thread-safe way.
"""

from core.file_system import FileSystem
from core.exceptions import InvalidPathFileSystemError, \
    AlreadyExistsFileSystemError
from core.exceptions import AccessFailedFileSystemError
import os, shutil

class DummyFileSystem(FileSystem):

    _real_root_dir = "temp"
    _total_space = 1000000000
    _space_used = 0

    def _real_path(self, path):
        """Returns the real path for the file or directory path input
        """
        if path[:1] is "/":
            root = os.path.abspath(self._real_root_dir)
            split = path.split("/")
            real_path = os.path.join(root, os.path.abspath(self._real_root_dir))

            if path is not "/":
                for splits in split:
                    real_path = os.path.join(real_path, splits)
        else:
            root = os.path.join(os.path.abspath(self._real_root_dir), self.working_dir[1:])
            real_path = os.path.join(root, path)
        return real_path

    def _virtual_path(self, path):
        """Returns the virtual path for the file or directory path input
        """

        if path[:2] == "..":
            if self.working_dir is "/":
                return "/"
            else:
                path = self.working_dir.rsplit("/", path.count("../") + 1)[0]
                if path == "":
                    path = "/"
        elif path[:1] == "/":
            pass
        elif path == ".":
            path = self.working_dir
        elif path[:2] == "./":
            path = path[2:]
            if path == "":
                path = self.working_dir
            else:
                path = self.working_dir + "/" + path
        else:
            if self.working_dir is "/":
                path = "/" + path
            else:
                path = self.working_dir + "/" + path

        return path

    @property
    def working_dir(self):
        return self._working_dir

    @working_dir.setter
    def working_dir(self, path):
        """Change the working directory.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """

        path = self._virtual_path(path)

        if not os.path.isdir(self._real_path(path)):
            raise InvalidPathFileSystemError()

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

    def list_dir(self, path=None):
        """Return the content of the specified directory. If no directory is specified, return the content of the current working directory.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
                
        The return value is a list of file and folder names. It does not contain references to the current
        or parent directory (e.g. « . » or « .. »).
        
        If the given path is invalid, raise InvalidPathError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        if path is None:
            path = self._real_path(self._working_dir)
            return os.listdir(os.path.abspath(path))
        else:
            path = self._real_path(path)
            if os.path.isdir(path):
                try:
                    return os.listdir(path)
                except:
                    raise AccessFailedFileSystemError()


    def is_dir(self, path):
        """Return a boolean value indicating if the given path corresponds to a directory.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise InvalidPathError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        path = self._real_path(path)
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
        path = self._real_path(path)
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
        pass

    def get_created_datetime(self, path):
        """Return the date and time of creation of the file or directory corresponding to the given path.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        The return value is a datetime object.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass

    def get_modified_datetime(self, path):
        """Return the date and time of the last modification to the file or directory corresponding to the given path.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        The return value is a datetime object.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        pass

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

    def make_dir(self, path):
        """Creates a new directory corresponding to the given path.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the parent path is invalid, raise InvalidPathFileSystemError.
        If the given path corresponds to an existing file or directory, raise AlreadyExistsFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        path = self._real_path(path)
        if not os.path.isdir(path):
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
        pass

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

    def delete(self, path):
        """Delete the file or directory corresponding to the given path.
        
        If the given path corresponds to a directory that is not empty, all its files and subdirectories
        must be deleted first.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        path = self._real_path(path)
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
        else:
            raise InvalidPathFileSystemError()

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
        path = self._real_path(path)
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
        path = self._real_path(path)
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

        if not os.path.isdir(os.path.abspath(self._real_root_dir)):
            os.mkdir(self._real_root_dir)

        self.working_dir = "/"
