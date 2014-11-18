from threading import Thread

class FTPServerThread(Thread):
    """A thread for running a FTPServer instance."""

    ftp_server = None

    def __init__(self, ftp_server):
        """FTPServerThread initializer"""
        self.ftp_server = ftp_server
        super(FTPServerThread, self).__init__()

    def run(self):
        """Start the thread and the FTP server."""
        self.ftp_server.serve_forever()
