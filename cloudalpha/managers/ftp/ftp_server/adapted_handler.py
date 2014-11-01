from pyftpdlib.handlers import FTPHandler
from managers.ftp.ftp_server.adapted_file_producer import AdaptedFileProducer

class AdaptedHandler(FTPHandler):

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
            # Make sure that the requested offset is valid (within the
            # size of the file being resumed).
            # According to RFC-1123 a 554 reply may result in case that
            # the existing file cannot be repositioned as specified in
            # the REST.
            ok = 0
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
