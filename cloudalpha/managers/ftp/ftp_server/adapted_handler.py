from pyftpdlib.handlers import FTPHandler

class AdaptedHandler(FTPHandler):

    def __init__(self, conn, server, ioloop=None):
        FTPHandler.__init__(self, conn, server, ioloop)
