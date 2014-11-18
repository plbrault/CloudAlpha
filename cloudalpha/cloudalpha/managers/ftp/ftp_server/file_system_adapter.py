from pyftpdlib.filesystems import AbstractedFS, FilesystemError as FTPError
from cloudalpha.exceptions import InvalidPathFileSystemError, InvalidTargetFileSystemError, AccessFailedFileSystemError, AlreadyExistsFileSystemError
from cloudalpha.managers.ftp.ftp_server.stat_result import StatResult

class FileSystemAdapter(AbstractedFS):
    """An adapter between pyftpdlib and cloudalpha.file_system_view.FileSystemView."""

    _next_class_id = 0
    _listed_dirs = {}

    file_system_view = None

    def _subclass_init(self, root, cmd_channel):
        self.cmd_channel = cmd_channel

    @staticmethod
    def get_class(file_system_view):
        """Create a new FileSystemAdapter subclass bound to the given FileSystemView instance."""
        FileSystemAdapter._next_class_id += 1
        return type("FileSystemAdapter_cls" + str(FileSystemAdapter._next_class_id), (FileSystemAdapter,),
                    {"__init__":FileSystemAdapter._subclass_init, "file_system_view":file_system_view})

    @property
    def cwd(self):
        """Return the current working directory."""
        return self.file_system_view.working_dir

    @cwd.setter
    def cwd(self, path):
        """Set the current working directory."""
        try:
            self.file_system_view.working_dir = path
        except InvalidPathFileSystemError:
            raise FTPError("No such file or directory")
        except InvalidTargetFileSystemError:
            raise FTPError("Not a directory")
        except AccessFailedFileSystemError:
            raise FTPError("File system currently inaccessible")

    @property
    def root(self):
        """Return the root path of the file system."""
        return "/"

    @root.setter
    def root(self, path):
        """Override the root setter of the base class to make it useless."""
        pass

    def ftpnorm(self, path):
        """Return the absolute path corresponding to the given relative path."""
        return self.file_system_view.get_abs_path(path.replace("\\", "/"))

    def ftp2fs(self, ftppath):
        """Same as ftpnorm."""
        return self.ftpnorm(ftppath)

    def fs2ftp(self, fspath):
        """Return fspath as is."""
        return fspath

    def validpath(self, path):
        """Return true if the given path starts with "/"."""
        return path.startswith("/")

    def open(self, filename, mode):
        """Override the open method of the base class to make it useless."""
        pass

    def chdir(self, path):
        """Change the current directory."""
        self.cwd = path

    def mkdir(self, path):
        """Create the specified directory."""
        try:
            self.file_system_view.make_dir(path)
        except InvalidPathFileSystemError:
            raise FTPError("Invalid path for new directory")
        except AlreadyExistsFileSystemError:
            raise FTPError("Can't create directory: File exists")
        except AccessFailedFileSystemError:
            raise FTPError("File system currently inaccessible")

    def listdir(self, path):
        """List the content of a directory."""
        if path[-1] != "/":
            path += "/"
        try:
            self._listed_dirs[path] = self.file_system_view.get_content_metadata(path)
            res = []
            for metadata in self._listed_dirs[path]:
                res.append(metadata.name)
            return res
        except InvalidPathFileSystemError:
            raise FTPError("No such file or directory")
        except InvalidTargetFileSystemError:
            raise FTPError("Not a directory")
        except AccessFailedFileSystemError:
            raise FTPError("File system currently inaccessible")

    def rmdir(self, path):
        """Remove the specified directory."""
        with self.file_system_view.lock:
            try:
                if self.file_system_view.is_dir(path):
                        self.file_system_view.delete(path)
                else:
                    raise FTPError("Not a directory")
            except InvalidPathFileSystemError:
                raise FTPError("No such file or directory")
            except AccessFailedFileSystemError:
                raise FTPError("File system currently inaccessible")

    def remove(self, path):
        """Remove the specified file."""
        with self.file_system_view.lock:
            try:
                if self.file_system_view.is_file(path):
                    self.file_system_view.delete(path)
                else:
                    raise FTPError("Given path points to a directory")
            except InvalidPathFileSystemError:
                raise FTPError("No such file or directory")
            except AccessFailedFileSystemError:
                raise FTPError("File system currently inaccessible")
            except:
                raise FTPError("Operation failed due to external modification of file system")


    def rename(self, src, dst):
        """Rename the specified src file to the dst filename."""
        with self.file_system_view.lock:
            try:
                if not self.file_system_view.exists(src):
                    raise FTPError("No such file or directory")
                if dst.rsplit("/", 1)[0].startswith(src):
                    raise FTPError("Cannot move source to the given destination")
                if self.file_system_view.exists(dst):
                    self.file_system_view.delete(dst)
                self.file_system_view.move(src, dst)
            except AccessFailedFileSystemError:
                raise FTPError("File system currently inaccessible")
            except:
                raise FTPError("Operation failed due to external modification of file system")


    def chmod(self, path, mode):
        """Override the chmod method of the base class to make it useless."""
        pass

    def metadata(self, path):
        """Return a FileMetadata object corresponding to path."""
        path = self.ftpnorm(path)
        if path[-1] == "/":
            path = path[:-1]
        path_split = path.rsplit("/", 1)
        parent_path = path_split[0]
        filename = path_split[-1]
        meta = None
        if parent_path in self._listed_dirs:
            for content_meta in self._listed_dirs[parent_path]:
                if content_meta.name == filename:
                    meta = content_meta
        if meta == None:
            try:
                meta = self.file_system_view.get_metadata(path)
            except InvalidPathFileSystemError:
                raise FTPError("No such file or directory")
            except AccessFailedFileSystemError:
                raise FTPError("File system currently inaccessible")
        return meta

    def stat(self, path):
        """Emulate a stat() system call on the given path."""
        meta = self.metadata(path)
        mode = StatResult.Modes.FILE
        if meta.is_dir:
            mode = StatResult.Modes.DIRECTORY
        return StatResult(mode, meta.size, meta.accessed_datetime.timestamp(), meta.modified_datetime.timestamp(), meta.created_datetime.timestamp())

    def lstat(self, path):
        """Same as stat."""
        return self.stat(path)

    def readlink(self, path):
        """Return the given path as is."""
        return path

    def isfile(self, path):
        """Return True if path is a file."""
        return not self.metadata(path).is_dir

    def islink(self, path):
        """Return False."""
        return False

    def isdir(self, path):
        """Return True if path is a directory."""
        return self.metadata(path).is_dir

    def getsize(self, path):
        """Return the size of the specified file in bytes."""
        return self.metadata(path).size

    def getmtime(self, path):
        """Return the last modified time of path as a number of seconds since the epoch."""
        return self.metadata(path).modified_datetime.timestamp()

    def realpath(self, path):
        """Return the given path as is."""
        return path

    def lexists(self, path):
        """Same as validpath."""
        return self.validpath(path)

    def get_user_by_uid(self, uid):
        """Return the string "owner"."""
        return "owner"

    def get_group_by_gid(self, gid):
        """Return the string "group"."""
        return "group"
