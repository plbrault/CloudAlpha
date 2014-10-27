from pyftpdlib.filesystems import AbstractedFS

class FileSystemAdapter(AbstractedFS):

    _next_class_id = 0
    _file_system_view = None

    def _subclass_init(self, root, cmd_channel):
        self.cmd_channel = cmd_channel

    @staticmethod
    def get_class(file_system_view):
        """Create a new FileSystemAdapter subclass bound to the given FileSystemView instance."""
        FileSystemAdapter._next_class_id += 1
        return type("FileSystemAdapter_cls" + str(FileSystemAdapter._next_class_id), (FileSystemAdapter,),
                    {"__init__":FileSystemAdapter._subclass_init, "_file_system_view":file_system_view})

    @property
    def cwd(self):
        """Return the current working directory."""
        return self._file_system_view.working_dir

    @cwd.setter
    def cwd(self, path):
        """Set the current working directory."""
        self._file_system_view.working_dir = path

    @property
    def root(self):
        """Return the root path of the file system."""
        return "/"

    @root.setter
    def root(self, path):
        """Override the root setter of the base class to make it effectless"""
        pass

    def ftpnorm(self, path):
        """Return the absolute path corresponding to the given relative path."""
        return self._file_system_view.get_abs_path(path)

    def ftp2fs(self, ftppath):
        """Same as ftpnorm."""
        return self.ftpnorm(ftppath)

    def fs2ftp(self, fspath):
        """Return fspath as is."""
        return fspath

    def validpath(self, path):
        """Return true if the given path is valid."""
        return self._file_system_view.exists(path)

    def open(self, filename, mode):
        pass

    def mkstemp(self, suffix='', prefix='', dir=None, mode='wb'):
        pass

    def chdir(self, path):
        """Change the current directory."""
        self._file_system_view.working_dir = path

    def mkdir(self, path):
        pass

    def listdir(self, path):
        """List the content of a directory."""
        return self._file_system_view.list_dir(path)

    def rmdir(self, path):
        pass

    def remove(self, path):
        pass

    def rename(self, src, dst):
        pass

    def chmod(self, path, mode):
        pass

    def stat(self, path):
        """Emulate a stat() system call on the given path."""
        class StatResult():
            st_mode = None
            st_ino = 0
            st_dev = 0
            st_nlink = 1
            st_uid = 0
            st_gid = 0
            st_size = None
            st_atime = None
            st_mtime = None
            st_ctime = None
            def __init__(self, mode, size, accessed_time, modified_time, created_time):
                self.st_mode = mode
                self.st_size = size
                self.st_atime = accessed_time
                self.st_mtime = modified_time
                self.st_ctime = created_time
            class Modes:
                FILE = 33206
                DIRECTORY = 16895
        mode = StatResult.Modes.FILE
        if self.isdir(path):
            mode = StatResult.Modes.DIRECTORY
        size = self.getsize(path)
        accessed_datetime = self._file_system_view.get_accessed_datetime(path)
        modified_datetime = self._file_system_view.get_modified_datetime(path)
        created_datetime = self._file_system_view.get_created_datetime(path)
        return StatResult(mode, size, accessed_datetime.timestamp(), modified_datetime.timestamp(), created_datetime.timestamp())

    def lstat(self, path):
        """Same as stat."""
        return self.stat(path)

    def readlink(self, path):
        """Return the given path as is."""
        return path

    def isfile(self, path):
        """Return True if path is a file."""
        return self._file_system_view.is_file(path)

    def islink(self, path):
        """Return False."""
        return False

    def isdir(self, path):
        """Return True if path is a directory."""
        return self._file_system_view.is_dir(path)

    def getsize(self, path):
        """Return the size of the specified file in bytes."""
        if not self._file_system_view.is_file(path):
            return 0
        return self._file_system_view.get_size(path)

    def getmtime(self, path):
        """Return the last modified time of path as a number of seconds since the epoch."""
        return self._file_system_view.get_modified_datetime(path).timestamp()

    def realpath(self, path):
        """Return the given path as is."""
        return path

    def lexists(self, path):
        """Same as validpath."""
        return self.validpath(path)

    def get_user_by_uid(self, uid):
        """Return the value "owner"."""
        return "owner"

    def get_group_by_gid(self, gid):
        """Return the value "group"."""
        return "group"
