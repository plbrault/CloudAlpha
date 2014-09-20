from pyftpdlib.filesystems import AbstractedFS
from pyftpdlib._compat import unicode, property
from datetime import datetime
import os

class File():
    size = None
    created_time = None
    modified_time = None
    access_time = None    
    
    def __init__(self, size, created_time, modified_time, access_time):
        self.size = size
        self.created_time = created_time
        self.modified_time = modified_time
        self.access_time = access_time
    
class Directory():
    content = None
    
    def __init__(self):
        self.content = {}

class FileSystem(AbstractedFS):

    root_dir = Directory()
    _root = "/"
    _cwd = "/"
    
    
    def __init__(self, root, cmd_channel):
        print("init", root, cmd_channel)
        
        dir1 = Directory()
        
        self.root_dir.content["dir1"] = dir1
        self.root_dir.content["file4"] = File(1024, datetime(2014,1,1,10,33), datetime(2014,1,1,10,33), datetime(2014,1,1,10,33))
        self.root_dir.content["file5"] = File(1024, datetime(2014,1,1,10,33), datetime(2014,1,1,10,33), datetime(2014,1,1,10,33))
        
        dir1.content["file1"] = File(1024, datetime(2014,1,1,10,33), datetime(2014,1,1,10,33), datetime(2014,1,1,10,33))
        dir1.content["file2"] = File(1024, datetime(2014,1,1,10,33), datetime(2014,1,1,10,33), datetime(2014,1,1,10,33))
        dir1.content["file3"] = File(1024, datetime(2014,1,1,10,33), datetime(2014,1,1,10,33), datetime(2014,1,1,10,33))
        
        super(FileSystem, self).__init__("/", cmd_channel)
        self._cwd = self._root
        
    @property
    def root(self):
        print("root")
        return self._root
    
    @property
    def cwd(self):
        print("cwd")
        return self._cwd
    
    @root.setter
    def root(self, path):
        print("root.setter", path)
        assert isinstance(path, unicode), path
        self._root = path       
    
    @cwd.setter
    def cwd(self, path):
        print("cwd.setter", path)
        assert isinstance(path, unicode), path
        self._cwd = path   
    
    def ftpnorm(self, ftppath):
        print("ftpnorm", ftppath)
        return ftppath.replace("\\", "/")
    
    def ftp2fs(self, ftppath):
        print("ftp2fs", ftppath)
        return ftppath
    
    def fs2ftp(self, fspath):
        print("fs2ftp", fspath)
        return super(FileSystem, self).fs2ftp(fspath)
    
    def validpath(self, path):
        print("validpath", path)
        path = self.ftpnorm(path)
        levels = path.split("/")
        cur = self.root_dir
        for level in levels:
            if level != '':
                if level in cur.content:
                    cur = cur.content[level]
                else:
                    return False
        return True
    
    def open(self, filename, mode):
        print("open", filename, mode)
        return super(FileSystem, self).open(filename, mode)
    
    def mkstemp(self, suffix='', prefix='', dir=None, mode='wb'):
        print("mkstemp", suffix, prefix, dir, mode)
        return super(FileSystem, self).mkstemp(suffix, prefix, dir, mode)
    
    def chdir(self, path):
        print("chdir", path)
        return super(FileSystem, self).chdir(path)
    
    def mkdir(self, path):
        print("mkdir", path)
        return super(FileSystem, self).mkdir(path)
    
    def listdir(self, path):
        print("listdir", path)
        levels = path.split("/")
        cur = self.root_dir
        for level in levels:
            if level != '':
                if level in cur.content:
                    cur = cur.content[level]
        return list(cur.content.keys())
    
    def rmdir(self, path):
        print("rmdir", path)
        return super(FileSystem, self).rmdir(path)
    
    def remove(self, path):
        print("remove", path)
        return super(FileSystem, self).remove(path)
    
    def rename(self, src, dst):
        print("rename", src, dst)
        return super(FileSystem, self).rename(src, dst)
    
    def chmod(self, path, mode):
        print("chmod", mode)
        return super(FileSystem, self).chmod(path, mode)
    
    def stat(self, path):
        print("stat", path)
        return os.stat("C:\\")
    
    def lstat(self, path):
        print("lstat", path)
        return super(FileSystem, self).lstat(path)
        
    def readlink(self, path):
        print("readlink", path)
        return super(FileSystem, self).readlink(path)
    
    def isfile(self, path):
        print("isfile")
        levels = path.split("/")
        cur = self.root_dir
        for level in levels:
            if level in cur.content:
                cur = cur.content[level]
        return type(cur) is File
    
    def islink(self, path):
        print("islink")
        return False    
    
    def isdir(self, path):
        print("isdir", path)
        levels = path.split("/")
        cur = self.root_dir
        for level in levels:
            if level in cur.content:
                cur = cur.content[level]
        return type(cur) is Directory

    def getsize(self, path):
        print("getsize", path)
        return 1024

    def getmtime(self, path):
        print("getmtime", path)
        return 1411084800

    def realpath(self, path):
        print("realpath", path)
        return path
    
    def lexists(self, path):
        print("lexists", path)
        return super(FileSystem, self).lexists(path)
    
    def get_user_by_uid(self, uid):
        print("get_user_by_uid", uid)
        return super(FileSystem, self).get_user_by_uid(uid)
    
    def get_group_by_gid(self, gid):
        print("get_group_by_gid", gid)
        return super(FileSystem, self).get_group_by_gid(gid)
    
    def get_list_dir(self, path):
        print("get_list_dir", path)
        return super(FileSystem, self).get_list_dir(path)
    
    def format_list(self, basedir, listing, ignore_err=True):
        print("format_list", basedir, listing, ignore_err)
        return super(FileSystem, self).format_list(basedir, listing, ignore_err)
    
    def format_mlsx(self, basedir, listing, perms, facts, ignore_err=True):
        print("format_mlsx", basedir, listing, perms, facts, ignore_err)
        return super(FileSystem, self).format_mlsx(basedir, listing, perms, facts, ignore_err)