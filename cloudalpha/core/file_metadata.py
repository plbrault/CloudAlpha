class FileMetadata(object):
    """Represent the metadata of a file."""

    path = ""
    is_dir = False
    size = 0
    created_datetime = None
    accessed_datetime = None
    modified_datetime = None

    @property
    def name(self):
        path = self.path
        if path[-1:] == "/":
            path = path[:-1]
        return path.rsplit("/", 1)[-1]

    def __init__(self, path="", is_dir=False, size=0, created_datetime=None, accessed_datetime=None, modified_datetime=None):
        self.path = path
        self.is_dir = is_dir
        self.size = size
        self.created_datetime = created_datetime
        self.accessed_datetime = accessed_datetime
        self.modified_datetime = modified_datetime

    def __str__(self):
        return ('FileMetadata(path="' + self.path + '", name="' + self.name + '", is_dir=' + str(self.is_dir) + ", size=" + str(self.size)
            + ", created_datetime=" + str(self.created_datetime) + ", accessed_datetime=" + str(self.accessed_datetime)
            + ", modified_datetime=" + str(self.modified_datetime) + ")")
