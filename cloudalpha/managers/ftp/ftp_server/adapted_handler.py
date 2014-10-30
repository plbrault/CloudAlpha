from pyftpdlib.handlers import FTPHandler

class AdaptedHandler(FTPHandler):

    def __init__(self, conn, server, ioloop=None):
        super(FTPHandler, self).__init__(conn, server, ioloop)
