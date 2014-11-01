from pyftpdlib.handlers import FTPHandler
from managers.ftp.ftp_server.adapted_file_producer import AdaptedFileProducer
from managers.ftp.ftp_server.adapted_dtp_handler import AdaptedDTPHandler

class AdaptedFTPHandler(FTPHandler):

    dtp_handler = AdaptedDTPHandler

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

#     def ftp_STOR(self, file, mode='w'):
#         if 'a' in mode:
#             cmd = 'APPE'
#         else:
#             cmd = 'STOR'
#         rest_pos = self._restart_position
#         self._restart_position = 0
#         if rest_pos:
#             mode = 'r+'
#
#
#         if self.data_channel is not None:
#             resp = "Data connection already open. Transfer starting."
#             self.respond("125 " + resp)
#
#
#             self.data_channel.file_obj = fd
#             self.data_channel.enable_receiving(self._current_type, cmd)
#
#
#         else:
#             resp = "File status okay. About to open data connection."
#             self.respond("150 " + resp)
#
#
#             self._in_dtp_queue = (fd, cmd)
#         return file
