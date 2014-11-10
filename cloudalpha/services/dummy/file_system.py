import os
import shutil
from threading import RLock
from datetime import datetime

from core.exceptions import InvalidPathFileSystemError, \
    AlreadyExistsFileSystemError, InvalidTargetFileSystemError, \
    AccessFailedFileSystemError, UncommittedExistsFileSystemError, \
    ForbiddenOperationFileSystemError, InsufficientSpaceFileSystemError
from core.file_system import FileSystem


class DummyFileSystem(FileSystem):

    _REAL_ROOT_DIR = ".dummyroot"
    _TEMP_DIR = ".dummytemp"

    _total_space = 1000000000
    _space_used = 0
    _new_files = {}

    _lock = RLock()

    @property
    def lock(self):
        """Return the Lock object for the current instance."""
        return self._lock

    def _get_real_path(self, path):
        """Return the real path corresponding to the specified virtual path.
        """
        return os.path.abspath(os.path.join(self._REAL_ROOT_DIR, path[1:]))

    @property
    def space_used(self):
        """Return the number of bytes used on the file system.
        
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        with self._lock:
            return self._space_used

    @property
    def free_space(self):
        """Return the free space remaining on the file system, in bytes.
        
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        with self._lock:
            return self._total_space - self._space_used

    def exists(self, path):
        """Return True if the given path points to an existing file or directory, excluding uncommitted files.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If the real file system is inaccessible, raise AccessFailedFileSystemError.        
        """
        with self._lock:
            return os.path.exists(self._get_real_path(path))

    def list_dir(self, path):
        """Return the content of the specified directory. If no directory is specified, return the content of the current working directory.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
                
        The return value is a list of file and folder names. It does not contain references to the current
        or parent directory (e.g. « . » or « .. »).
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the given path does not correspond to a directory, raise InvalidTargetFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        with self._lock:
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
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        with self._lock:
            path = self._get_real_path(path)
            if not os.path.exists(path):
                raise InvalidPathFileSystemError
            return os.path.isdir(path)

    def is_file(self, path):
        """Return a boolean value indicating if the given path corresponds to a file.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        with self._lock:
            path = self._get_real_path(path)
            if not os.path.exists(path):
                raise InvalidPathFileSystemError
            return os.path.isfile(path)

    def get_size(self, path):
        """Return the size, in bytes, of the file corresponding to the given path.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the given path corresponds to a directory, raise InvalidTargetFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError. 
        """
        with self._lock:
            path = self._get_real_path(path)
            if not os.path.exists(path):
                raise InvalidPathFileSystemError()
            if os.path.isdir(path):
                raise InvalidTargetFileSystemError()
            try:
                return os.path.getsize(path)
            except:
                raise AccessFailedFileSystemError()

    def get_created_datetime(self, path):
        """Return the date and time of creation of the file or directory corresponding to the given path.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        The return value is a datetime object.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        with self._lock:
            path = self._get_real_path(path)
            if not os.path.exists(path):
                raise InvalidPathFileSystemError
            try:
                return datetime.fromtimestamp(os.path.getctime(path))
            except:
                raise AccessFailedFileSystemError()

    def get_modified_datetime(self, path):
        """Return the date and time of the last modification to the file or directory corresponding to the given path.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        The return value is a datetime object.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        with self._lock:
            path = self._get_real_path(path)
            if not os.path.exists(path):
                raise InvalidPathFileSystemError
            try:
                return datetime.fromtimestamp(os.path.getmtime(path))
            except:
                raise AccessFailedFileSystemError()

    def get_accessed_datetime(self, path):
        """Return the date and time of the last time the given file or directory was accessed.
        If not available, return the date and time of the last modification.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        The return value is a datetime object.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        with self._lock:
            path = self._get_real_path(path)
            if not os.path.exists(path):
                raise InvalidPathFileSystemError
            try:
                return datetime.fromtimestamp(os.path.getatime(path))
            except:
                raise AccessFailedFileSystemError()

    def make_dir(self, path):
        """Creates a new directory corresponding to the given path.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If the parent path is invalid, raise InvalidPathFileSystemError.
        If the given path corresponds to an existing file or directory, raise AlreadyExistsFileSystemError.
        If the given path corresponds to an uncommitted file or directory, raise UncommittedExistsFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        with self._lock:
            real_path = self._get_real_path(path)
            real_parent_path = real_path.rsplit("/", 1)[0].rsplit("\\", 1)[0]
            if not os.path.exists(real_parent_path):
                raise InvalidPathFileSystemError()
            if os.path.exists(real_path):
                raise AlreadyExistsFileSystemError()
            if path in self._new_files:
                raise UncommittedExistsFileSystemError()
            try:
                os.mkdir(real_path)
            except:
                raise AccessFailedFileSystemError()

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
        with self._lock:
            real_old_path = self._get_real_path(old_path)
            real_new_path = self._get_real_path(new_path)
            if not os.path.exists(real_old_path):
                raise InvalidPathFileSystemError()
            if os.path.exists(real_new_path):
                raise AlreadyExistsFileSystemError()
            if new_path in self._new_files:
                raise UncommittedExistsFileSystemError()
            try:
                shutil.move(real_old_path, real_new_path)
            except PermissionError:
                raise ForbiddenOperationFileSystemError()
            except:
                raise AccessFailedFileSystemError()

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
        with self._lock:
            real_path = self._get_real_path(path)
            real_copy_path = self._get_real_path(copy_path)
            if not os.path.exists(real_path):
                raise InvalidPathFileSystemError()
            if real_path in real_copy_path:
                raise ForbiddenOperationFileSystemError()
            if os.path.exists(real_copy_path):
                raise AlreadyExistsFileSystemError()
            if copy_path in self._new_files:
                raise UncommittedExistsFileSystemError()
            try:
                if os.path.isdir(real_path):
                    shutil.copytree(real_path, real_copy_path)
                else:
                    shutil.copy(real_path, real_copy_path)
            except:
                raise AccessFailedFileSystemError()

    def delete(self, path):
        """Delete the file or directory corresponding to the given path.
        
        If the given path corresponds to a directory that is not empty, all its files and subdirectories
        must be deleted first.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        with self._lock:
            path = self._get_real_path(path)
            if os.path.exists(path):
                try:
                    if os.path.isdir(path):
                        dir_size = 0
                        for dir_path, dir_names, filenames in os.walk(path):
                            for f in filenames:
                                fp = os.path.join(dir_path, f)
                                dir_size += os.path.getsize(fp)
                        self._space_used -= dir_size
                        shutil.rmtree(path)
                    else:
                        self._space_used -= os.path.getsize(path)
                        os.remove(path)
                except:
                    raise AccessFailedFileSystemError()
            else:
                raise InvalidPathFileSystemError()

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
        with self._lock:
            real_path = self._get_real_path(path)
            if not os.path.exists(real_path):
                raise InvalidPathFileSystemError()
            if os.path.isdir(real_path):
                raise InvalidTargetFileSystemError()
            if num_bytes == None:
                num_bytes = self.get_size(path) - start_byte
            try:
                file = open(real_path, 'rb')
                file.seek(start_byte)
                data = bytearray(file.read(num_bytes))
                file.close()
                return data
            except:
                raise AccessFailedFileSystemError()

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
        with self._lock:
            real_path = self._get_real_path(path)
            real_parent_path = real_path.rsplit("/", 1)[0].rsplit("\\", 1)[0]
            if not os.path.exists(real_parent_path):
                raise InvalidPathFileSystemError()
            if os.path.isdir(real_path):
                raise InvalidTargetFileSystemError()
            if path in self._new_files:
                raise UncommittedExistsFileSystemError()
            try:
                temp_dir_path = os.path.abspath(self._TEMP_DIR)
                virtual_path_split = path.split("/")
                for level in virtual_path_split[:-1]:
                    temp_dir_path = os.path.join(temp_dir_path, level)
                    if not os.path.exists(temp_dir_path):
                        os.mkdir(temp_dir_path)
                temp_file_path = os.path.join(temp_dir_path, virtual_path_split[-1:][0])
                self._new_files[path] = (caller_unique_id, open(temp_file_path, "ab"))
                if os.path.exists(real_path):
                    self._space_used -= os.path.getsize(real_path)
            except:
                raise AccessFailedFileSystemError()

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
        with self._lock:
            if path not in self._new_files:
                raise InvalidTargetFileSystemError()
            if len(data) > self.free_space:
                raise InsufficientSpaceFileSystemError()
            self._space_used += len(data)
        creator_unique_id, temp_file = self._new_files[path]
        if caller_unique_id == creator_unique_id:
            try:
                temp_file.write(data)
            except:
                with self._lock:
                    self._space_used -= len(data)
                raise AccessFailedFileSystemError()
        else:
            raise ForbiddenOperationFileSystemError()

    def commit_new_file(self, caller_unique_id, path):
        """Commit a file that was previously created/overwritten, then populated with data.
        
        The caller_unique_id is used to ensure that only the file creator can commit it.
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.     
        
        If the given path does not correspond to an uncommitted file, raise InvalidTargetFileSystemError.
        If caller_unique_id does not correspond to the unique_id of the file creator, raise ForbiddenOperationFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        with self._lock:
            if path not in self._new_files:
                raise InvalidTargetFileSystemError()
            creator_unique_id, temp_file = self._new_files.pop(path)[:2]
            if caller_unique_id == creator_unique_id:
                try:
                    temp_file.close()
                except:
                    pass
                try:
                    abs_temp_path = os.path.abspath(os.path.join(self._TEMP_DIR, path[1:]))
                    abs_real_path = self._get_real_path(path)
                    shutil.move(abs_temp_path, abs_real_path)
                except:
                    raise AccessFailedFileSystemError()
            else:
                raise ForbiddenOperationFileSystemError()

    def flush_new_file(self, caller_unique_id, path):
        """Delete an uncommitted file.
        
        The caller_unique_id is used to ensure that only the file creator can flush it.
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If the given path does not correspond to an uncommitted file, raise InvalidTargetFileSystemError.
        If caller_unique_id does not correspond to the unique_id of the file creator, raise ForbiddenOperationFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.                
        """
        with self._lock:
            real_path = self._get_real_path(path)
            if path not in self._new_files:
                raise InvalidTargetFileSystemError()
            creator_unique_id, temp_file = self._new_files.pop(path)
            if caller_unique_id == creator_unique_id:
                try:
                    self._space_used -= temp_file.tell()
                    temp_file.close()
                    if os.path.exists(real_path):
                        self._space_used -= os.path.getsize(real_path)
                except:
                    pass
                try:
                    real_temp_path = os.path.abspath(os.path.join(self._TEMP_DIR, path[1:]))
                    os.remove(real_temp_path)
                except:
                    raise AccessFailedFileSystemError()
            else:
                raise ForbiddenOperationFileSystemError()

    def new_file_exists(self, path):
        """Return True if the given path corresponds to an uncommitted file.
        
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        with self._lock:
            return path in self._new_files

    def __init__(self, account):
        """DummyFileSystem initializer"""
        super(DummyFileSystem, self).__init__(account)
        root = os.path.abspath(self._REAL_ROOT_DIR)
        temp = os.path.abspath(self._TEMP_DIR)
        if os.path.exists(root):
            if os.path.isdir(root):
                shutil.rmtree(root, True)
            else:
                os.remove(root)
        if os.path.exists(temp):
            if os.path.isdir(temp):
                shutil.rmtree(temp, True)
            else:
                os.remove(temp)
        os.mkdir(root)
        os.mkdir(temp)
