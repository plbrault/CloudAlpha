from pyftpdlib.handlers import FTPHandler
from cloudalpha.managers.ftp.ftp_server.adapted_file_producer import AdaptedFileProducer
from cloudalpha.managers.ftp.ftp_server.adapted_dtp_handler import AdaptedDTPHandler

class AdaptedFTPHandler(FTPHandler):
    """FTPHandler is the class that handles FTP commands received from the client.
    AdaptedFTPHandler inherits from it to adapt the handling of STOR and RETR
    commands to the use of cloudalpha.file_system.FileSystem subclasses.
    """

    dtp_handler = AdaptedDTPHandler

    upload_path = None

    def __init__(self, conn, server, ioloop=None):
        FTPHandler.__init__(self, conn, server, ioloop)

    def ftp_RETR(self, file):
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
        """Store a file (transfer from the client to the server).
        On success return the file path, else None.
        """
        self.upload_path = file
        super(AdaptedFTPHandler, self).ftp_STOR(file, mode)

    def ftp_STOU(self, line):
        """Return an error message indicating that the server
        does not support the STOU command.
        """
        self.respond("500 Syntax error, command unrecognized.")
