from pyftpdlib.handlers import FTPHandler
from managers.ftp.ftp_server.adapted_file_producer import AdaptedFileProducer
from managers.ftp.ftp_server.adapted_dtp_handler import AdaptedDTPHandler

class AdaptedFTPHandler(FTPHandler):

    dtp_handler = AdaptedDTPHandler

    upload_path = None

    def __init__(self, conn, server, ioloop=None):
        FTPHandler.__init__(self, conn, server, ioloop)

    def ftp_RETR(self, file):
        print("ftp_RETR", file)

        """Retrieve the specified file (transfer from the server to the
        client).  On success return the file path else None.
        """
        rest_pos = self._restart_position
        self._restart_position = 0

        if rest_pos:
            try:
                if rest_pos > self.fs.getsize(file):
                    raise ValueError
                ok = 1
            except ValueError:
                why = "Invalid REST parameter"
            if not ok:
                self.respond('554 %s' % why)
                return
        producer = AdaptedFileProducer(self.fs.file_system_view, file)
        self.push_dtp_data(producer, isproducer=True, cmd="RETR")
        return file

    def ftp_STOR(self, file, mode='w'):
        print("ftp_STOR")

        self.upload_path = file
        super(FTPHandler, self).ftp_STOR(file, mode)
