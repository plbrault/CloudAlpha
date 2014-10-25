from pyftpdlib.filesystems import AbstractedFS

class FileSystemAdapter(AbstractedFS):

    def __init__(self, root, cmd_channel):

        super(FileSystemAdapter, self).__init__("/", cmd_channel)
        self._cwd = self._root

    @property
    def root(self):
        pass

    @property
    def cwd(self):
        pass

    @root.setter
    def root(self, path):
        pass

    @cwd.setter
    def cwd(self, path):
        pass

    def ftpnorm(self, ftppath):
        pass

    def ftp2fs(self, ftppath):
        pass

    def fs2ftp(self, fspath):
        pass

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
