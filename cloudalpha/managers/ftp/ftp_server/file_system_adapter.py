from pyftpdlib.filesystems import AbstractedFS

class FileSystemAdapter(AbstractedFS):

    _next_class_id = 0
    _file_system_view = None

    def _subclass_init(self, root, cmd_channel):
        AbstractedFS.__init__(self, "/", cmd_channel)
        self._file_system_view.working_dir = root

    @staticmethod
    def get_class(file_system_view):
        """Create a new FileSystemAdapter subclass bound to the given FileSystemView instance."""
        FileSystemAdapter._next_class_id += 1
        return type("FileSystemAdapter_cls" + FileSystemAdapter._next_class_id, (FileSystemAdapter,),
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
        pass

    def open(self, filename, mode):
        pass

    def mkstemp(self, suffix='', prefix='', dir=None, mode='wb'):
        pass

    def chdir(self, path):
        pass

    def mkdir(self, path):
        pass

    def listdir(self, path):
        pass

    def rmdir(self, path):
        pass

    def remove(self, path):
        pass

    def rename(self, src, dst):
        pass

    def chmod(self, path, mode):
        pass

    class StatResult():
        pass

    def stat(self, path):
        pass

    def lstat(self, path):
        pass

    def readlink(self, path):
        pass

    def isfile(self, path):
        pass

    def islink(self, path):
        pass

    def isdir(self, path):
        pass

    def getsize(self, path):
        pass

    def getmtime(self, path):
        pass

    def realpath(self, path):
        pass

    def lexists(self, path):
        pass

    def get_user_by_uid(self, uid):
        pass

    def get_group_by_gid(self, gid):
        pass

    def get_list_dir(self, path):
        pass

    def format_list(self, basedir, listing, ignore_err=True):
        pass

    def format_mlsx(self, basedir, listing, perms, facts, ignore_err=True):
        pass
