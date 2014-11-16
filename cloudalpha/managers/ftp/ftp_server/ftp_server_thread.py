from threading import Thread

class FTPServerThread(Thread):
    ftp_server = None

    def __init__(self, ftp_server):
        self.ftp_server = ftp_server
        super(FTPServerThread, self).__init__()

    def run(self):
        self.ftp_server.serve_forever()
