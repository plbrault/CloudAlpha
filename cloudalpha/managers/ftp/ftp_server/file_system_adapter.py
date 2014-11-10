from pyftpdlib.filesystems import AbstractedFS
from core.exceptions import InvalidPathFileSystemError, InvalidTargetFileSystemError

class FileSystemAdapter(AbstractedFS):

    _next_class_id = 0

    manager_unique_id = None
    file_system_view = None

    def _subclass_init(self, root, cmd_channel):
        self.cmd_channel = cmd_channel

    @staticmethod
    def get_class(manager_unique_id, file_system_view):
        print("get_class", file_system_view)

        """Create a new FileSystemAdapter subclass bound to the given FileSystemView instance."""
        FileSystemAdapter._next_class_id += 1
        return type("FileSystemAdapter_cls" + str(FileSystemAdapter._next_class_id), (FileSystemAdapter,),
                    {"__init__":FileSystemAdapter._subclass_init, "manager_unique_id":manager_unique_id, "file_system_view":file_system_view})

    @property
    def cwd(self):
        print("cwd")

        """Return the current working directory."""
        return self.file_system_view.working_dir

    @cwd.setter
    def cwd(self, path):
        print("cwd", path)

        """Set the current working directory."""
        self.file_system_view.working_dir = path

    @property
    def root(self):
        print("root")

        """Return the root path of the file system."""
        return "/"

    @root.setter
    def root(self, path):
        print("root", path)

        """Override the root setter of the base class to make it effectless"""
        pass

    def ftpnorm(self, path):
        print("ftpnorm", path)

        """Return the absolute path corresponding to the given relative path."""
        return self.file_system_view.get_abs_path(path.replace("\\", "/"))

    def ftp2fs(self, ftppath):
        print("ftp2fs", ftppath)

        """Same as ftpnorm."""
        return self.ftpnorm(ftppath)

    def fs2ftp(self, fspath):
        print("fs2ftp", fspath)

        """Return fspath as is."""
        return fspath

    def validpath(self, path):
        print("validpath", path)

        """Return true if the given path starts with "/"."""
        return path.startswith("/")

    def open(self, filename, mode):
        print("open", filename, mode)

        pass

    def mkstemp(self, suffix='', prefix='', dir=None, mode='wb'):
        print("mkstemp", suffix, prefix, dir, mode)

        pass

    def chdir(self, path):
        print("chdir", path)

        """Change the current directory."""
        try:
            self.file_system_view.working_dir = path
        except InvalidPathFileSystemError:
            raise FileNotFoundError
        except InvalidTargetFileSystemError:
            raise NotADirectoryError

    def mkdir(self, path):
        print("mkdir", path)

        """Create the specified directory."""
        self.file_system_view.make_dir(path)

    def listdir(self, path):
        print("listdir", path)

        """List the content of a directory."""
        return self.file_system_view.list_dir(path)

    def rmdir(self, path):
        print("rmdir", path)

        """Remove the specified directory."""
        self.file_system_view.delete(path)

    def remove(self, path):
        print("remove", path)

        """Remove the specified file."""
        self.file_system_view.delete(path)

    def rename(self, src, dst):
        print("rename", src, dst)

        """Rename the specified src file to the dst filename."""
        self.file_system_view.move(src, dst)

    def chmod(self, path, mode):
        print("chmod", path, mode)

        """Do nothing"""
        pass

    def stat(self, path):
        print("stat", path)

        """Emulate a stat() system call on the given path."""
        path = self.ftpnorm(path)
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
        accessed_datetime = self.file_system_view.get_accessed_datetime(path)
        modified_datetime = self.file_system_view.get_modified_datetime(path)
        created_datetime = self.file_system_view.get_created_datetime(path)
        return StatResult(mode, size, accessed_datetime.timestamp(), modified_datetime.timestamp(), created_datetime.timestamp())

    def lstat(self, path):
        print("lstat", path)

        """Same as stat."""
        return self.stat(path)

    def readlink(self, path):
        print("readlink", path)

        """Return the given path as is."""
        return path

    def isfile(self, path):
        print("isfile", path)

        """Return True if path is a file."""
        return self.file_system_view.is_file(path)

    def islink(self, path):
        print("islink", path)

        """Return False."""
        return False

    def isdir(self, path):
        print("isdir", path)

        """Return True if path is a directory."""
        return self.file_system_view.is_dir(path)

    def getsize(self, path):
        print("getsize", path)

        """Return the size of the specified file in bytes."""
        if not self.file_system_view.is_file(path):
            return 0
        return self.file_system_view.get_size(path)

    def getmtime(self, path):
        print("getmtime", path)

        """Return the last modified time of path as a number of seconds since the epoch."""
        return self.file_system_view.get_modified_datetime(path).timestamp()

    def realpath(self, path):
        print("realpath", path)

        """Return the given path as is."""
        return path

    def lexists(self, path):
        print("lexists", path)

        """Same as validpath."""
        return self.validpath(path)

    def get_user_by_uid(self, uid):
        print("get_user_by_uid", uid)

        """Return the value "owner"."""
        return "owner"

    def get_group_by_gid(self, gid):
        print("get_group_by_gid", gid)

        """Return the value "group"."""
        return "group"
