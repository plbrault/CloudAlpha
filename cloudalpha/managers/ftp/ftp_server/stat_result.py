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