from pyftpdlib.filesystems import AbstractedFS
from core.exceptions import InvalidPathFileSystemError, InvalidTargetFileSystemError
from managers.ftp.ftp_server.stat_result import StatResult

class FileSystemAdapter(AbstractedFS):

    _next_class_id = 0
    _listed_dirs = {}

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
        if path[-1] != "/":
            path += "/"
        self._listed_dirs[path] = self.file_system_view.get_content_metadata(path)
        res = []
        for metadata in self._listed_dirs[path]:
            res.append(metadata.name)
        return res

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

        """Do nothing."""
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
            meta = self.file_system_view.get_metadata(path)
        return meta

    def stat(self, path):
        print("stat", path)

        """Emulate a stat() system call on the given path."""
        meta = self.metadata(path)
        mode = StatResult.Modes.FILE
        if meta.is_dir:
            mode = StatResult.Modes.DIRECTORY
        return StatResult(mode, meta.size, meta.accessed_datetime.timestamp(), meta.modified_datetime.timestamp(), meta.created_datetime.timestamp())

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
        return not self.metadata(path).is_dir

    def islink(self, path):
        print("islink", path)

        """Return False."""
        return False

    def isdir(self, path):
        print("isdir", path)

        """Return True if path is a directory."""
        return self.metadata(path).is_dir

    def getsize(self, path):
        print("getsize", path)

        """Return the size of the specified file in bytes."""
        return self.metadata(path).size

    def getmtime(self, path):
        print("getmtime", path)

        """Return the last modified time of path as a number of seconds since the epoch."""
        return self.metadata(path).modified_datetime.timestamp()

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
