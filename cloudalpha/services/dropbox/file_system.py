from datetime import datetime
import os
from threading import RLock

from core.exceptions import AccessFailedFileSystemError, \
    AlreadyExistsFileSystemError, InvalidPathFileSystemError, \
    InvalidTargetFileSystemError, ForbiddenOperationFileSystemError, \
    UncommittedExistsFileSystemError, InsufficientSpaceFileSystemError
from core.file_system import FileSystem


class DropBoxFileSystem(FileSystem):

    _lock = RLock()
    _working_dir = '/'
    _new_files = {}
    _new_file_upload_ids = {}
    _uncomitted_file_space = 0
    _TEMP_DIR = ".dropboxtemp"

    @property
    def lock(self):
        """Return the Lock object for the current instance."""
        return self._lock

    @property
    def space_used(self):
        """Return the number of bytes used on the file system.
        
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        return self._client.account_info()["quota_info"]["normal"] + self._client.account_info()["quota_info"]["shared"]

    @property
    def free_space(self):
        """Return the free space remaining on the file system, in bytes.
        
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        return self._client.account_info()["quota_info"]["quota"] - self._client.account_info()["quota_info"]["normal"] - self._client.account_info()["quota_info"]["shared"]

    def exists(self, path):
        """Return True if the given path points to an existing file or directory, excluding uncommitted files.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If the real file system is inaccessible, raise AccessFailedFileSystemError.        
        """
        with self._lock:
            try:
                dropbox_meta = self._client.metadata(path)
                if dropbox_meta.get("is_deleted"):
                    return False
                else:
                    return True
            except Exception as e:
                if str(e).startswith("[404] \"Path \'"):
                    return False
                else:
                    raise AccessFailedFileSystemError()


    def list_dir(self, path):
        """Return the content of the specified directory. If no directory is specified, return the content of the current working directory.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
                
        The return value is a list of file and folder names. It does not contain references to the current
        or parent directory (e.g. « . » or « .. »).
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the given path does not correspond to a directory, raise InvalidTargetFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        items = []
        with self._lock:
            try:
                dropbox_meta = self._client.metadata(path)
                for contents in dropbox_meta["contents"]:
                    items.append(contents['path'].rsplit("/", 1)[1])
                return items
            except:
                raise AccessFailedFileSystemError()

    def is_dir(self, path):
        """Return a boolean value indicating if the given path corresponds to a directory.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        with self._lock:
            if self.exists(path):
                try:
                    dropbox_meta = self._client.metadata(path)
                    return dropbox_meta["is_dir"]
                except:
                    raise AccessFailedFileSystemError()
            else:
                raise InvalidPathFileSystemError()

    def is_file(self, path):
        """Return a boolean value indicating if the given path corresponds to a file.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        with self._lock:
            if self.exists(path):
                try:
                    dropbox_meta = self._client.metadata(path)
                    return not dropbox_meta["is_dir"]
                except:
                    raise AccessFailedFileSystemError()
            else:
                raise InvalidPathFileSystemError()

    def get_size(self, path):
        """Return the size, in bytes, of the file corresponding to the given path.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the given path corresponds to a directory, raise InvalidTargetFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError. 
        """
        with self._lock:
            if self.exists(path):
                if self.is_dir(path):
                    raise InvalidTargetFileSystemError()
                try:
                    dropbox_meta = self._client.metadata(path)
                    return dropbox_meta["bytes"]
                except:
                    raise AccessFailedFileSystemError()
            else:
                raise InvalidPathFileSystemError()

    def get_created_datetime(self, path):
        """Return the date and time of creation of the file or directory corresponding to the given path.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        The return value is a datetime object.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        with self._lock:
            try:
                dropbox_meta = self._client.metadata(path)
                return datetime.strptime(dropbox_meta["modified"], '%a, %d %b %Y %H:%M:%S +0000')
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
            try:
                dropbox_meta = self._client.metadata(path)
                return datetime.strptime(dropbox_meta["modified"], '%a, %d %b %Y %H:%M:%S +0000')
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
            try:
                dropbox_meta = self._client.metadata(path)
                return datetime.strptime(dropbox_meta["modified"], '%a, %d %b %Y %H:%M:%S +0000')
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
            if self.exists(path):
                raise AlreadyExistsFileSystemError()
            parentPath = path.rsplit("/", 1)[0]
            if not self.exists(parentPath):
                raise InvalidPathFileSystemError()
            try:
                self._client.file_create_folder(path)
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
            if not self.exists(old_path):
                raise InvalidPathFileSystemError()
            if self.exists(new_path):
                raise AlreadyExistsFileSystemError()
            if old_path in new_path.rsplit("/", 1)[0]:
                raise ForbiddenOperationFileSystemError()
            try:
                self._client.file_move(old_path, new_path)
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
            if not self.exists(path):
                raise InvalidPathFileSystemError()
            if self.exists(copy_path):
                raise AlreadyExistsFileSystemError()
            if path in copy_path.rsplit("/", 1)[0]:
                raise ForbiddenOperationFileSystemError()
            try:
                self._client.file_copy(path, copy_path)
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
            if not self.exists(path):
                raise InvalidPathFileSystemError()
            try:
                if self.is_dir(path):
                    dropbox_meta = self._client.metadata(path)
                    for contents in dropbox_meta["contents"]:
                        self.delete(contents.get("path"))
                self._client.file_delete(path)
            except:
                raise AccessFailedFileSystemError()

    def read(self, path, start_byte, num_bytes=None):
        """Read the number of bytes corresponding to num_bytes from the file corresponding to the given path,
        beginning at start_byte.
        
        If num_bytes is not specified, read all remaining bytes of the file.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        The return value is an iterable of bytes.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the given path corresponds to a directory, raise InvalidTargetFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
        """
        with self._lock:
            if not self.exists(path):
                raise InvalidPathFileSystemError()
            if self.is_dir(path):
                raise InvalidTargetFileSystemError()
            if num_bytes == None:
                num_bytes = self.get_size(path) - start_byte
            try:
                file = self._client.get_file(path, None, start_byte, num_bytes)
                data = file.read()
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
            parent_path = path.rsplit("/", 1)[0]
            if not self.exists(parent_path):
                raise InvalidPathFileSystemError()
            if self.exists(path):
                if self.is_dir(path):
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
            creator_unique_id, temp_file = self._new_files[path]
            if caller_unique_id == creator_unique_id:
                if len(data) > self.free_space:
                    raise InsufficientSpaceFileSystemError()
                try:
                    self._new_file_upload_ids[path] = self._client.upload_chunk(data, len(data), 0)[-1]
                except:
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
            creator_unique_id, temp_file = self._new_files.pop(path)
            upload_id = self._new_file_upload_ids.pop(path)
            if caller_unique_id == creator_unique_id:
                try:
                    temp_file.close()
                except:
                    pass
                try:
                    self._client.commit_chunked_upload("/auto/" + path.strip("/"), upload_id, True)
                except Exception as e:
                    print(e)
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
            if path not in self._new_files:
                raise InvalidTargetFileSystemError()
            creator_unique_id, temp_file, file_size = self._new_files.pop(path)
            self._new_file_upload_ids.pop(path)
            if caller_unique_id == creator_unique_id:
                try:
                    temp_file.close()
                    self._uncomitted_file_space -= file_size
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
        super(DropBoxFileSystem, self).__init__(account)
