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
        super(AdaptedFTPHandler, self).ftp_STOR(file, mode)




    ###### TEMP ######

    def handle(self):
        print("handle")
        return super(AdaptedFTPHandler, self).handle()

    def handle_max_cons(self):
        print("handle_max_cons")
        return super(AdaptedFTPHandler, self).handle_max_cons()

    def handle_max_cons_per_ip(self):
        print("handle_max_cons_per_ip")
        return super(AdaptedFTPHandler, self).handle_max_cons_per_ip()

    def handle_timeout(self):
        print("handle_timeout")
        return super(AdaptedFTPHandler, self).handle_timeout

    # --- asyncore / asynchat overridden methods

    print_readable = True
    def readable(self):
        if self.print_readable:
            print("readable")
            self.print_readable = False
        return super(AdaptedFTPHandler, self).readable()

    def writable(self):
        print("writable")
        return super(AdaptedFTPHandler, self).writable()

    def collect_incoming_data(self, data):
        print("collect_incoming_data", data)
        return super(AdaptedFTPHandler, self).collect_incoming_data(data)

    def decode(self, bytes):
        print("decode")
        return super(AdaptedFTPHandler, self).decode(bytes)

    def found_terminator(self):
        print("found_terminator")
        return super(AdaptedFTPHandler, self).found_terminator()

    def pre_process_command(self, line, cmd, arg):
        print("pre_process_command", line, cmd, arg)
        return super(AdaptedFTPHandler, self).pre_process_command(line, cmd, arg)

    def process_command(self, cmd, *args, **kwargs):
        print("process_command")
        return super(AdaptedFTPHandler, self).process_command(cmd, *args, **kwargs)

    def handle_error(self):
        print("handle_error")
        return super(AdaptedFTPHandler, self).handle_error()

    def handle_close(self):
        print("handle_close")
        return super(AdaptedFTPHandler, self).handle_close()

    def close(self):
        print("close")
        return super(AdaptedFTPHandler, self).close()

    def _shutdown_connecting_dtp(self):
        print("_shutdown_connecting_dtp")
        return super(AdaptedFTPHandler, self)._shutdown_connecting_dtp()

    # --- public callbacks
    # Note: to run a time consuming task make sure to use a separate
    # process or thread (see FAQs).

    def on_connect(self):
        print("on_connect")
        return super(AdaptedFTPHandler, self).on_connect()

    def on_disconnect(self):
        print("on_disconnect")
        return super(AdaptedFTPHandler, self).on_disconnect()

    def on_login(self, username):
        print("on_login")
        return super(AdaptedFTPHandler, self).on_login(username)

    def on_login_failed(self, username, password):
        print("on_login_failed")
        return super(AdaptedFTPHandler, self).on_login_failed

    def on_logout(self, username):
        print("on_logout")
        return super(AdaptedFTPHandler, self).on_logout(username)

    def on_file_sent(self, file):
        print("on_file_sent")
        return super(AdaptedFTPHandler, self).on_file_sent(file)

    def on_file_received(self, file):
        print("on_file_received")
        return super(AdaptedFTPHandler, self).on_file_received(file)

    def on_incomplete_file_sent(self, file):
        print("on_incomplete_file_sent")
        return super(AdaptedFTPHandler, self)._on_incomplete_file_sent(file)

    def on_incomplete_file_received(self, file):
        print("on_incomplete_file_received")
        return super(AdaptedFTPHandler, self).on_incomplete_file_received(file)

    # --- internal callbacks

    def _on_dtp_connection(self):
        print("_on_dtp_connection")
        return super(AdaptedFTPHandler, self)._on_dtp_connection()

    def _on_dtp_close(self):
        print("_on_dtp_close")
        return super(AdaptedFTPHandler, self)._on_dtp_close()

    # --- utility

    def push(self, s):
        print("push")
        return super(AdaptedFTPHandler, self).push(s)

    def respond(self, resp, logfun=None):
        print("respond", resp)
        if logfun is None:
            return super(AdaptedFTPHandler, self).respond(resp)
        else:
            return super(AdaptedFTPHandler, self).respond(resp, logfun)

    def respond_w_warning(self, resp):
        print("respond_w_warning")
        return super(AdaptedFTPHandler, self).respond_w_warning(resp)

    def push_dtp_data(self, data, isproducer=False, file=None, cmd=None):
        print("push_dtp_data")
        return super(AdaptedFTPHandler, self).push_dtp_data(data, isproducer, file, cmd)

    def flush_account(self):
        print("flush_account")
        return super(AdaptedFTPHandler, self).flush_account()

    def run_as_current_user(self, function, *args, **kwargs):
        print("run_as_current_user")
        return super(AdaptedFTPHandler, self).run_as_current_user(function, *args, **kwargs)

    # --- logging wrappers

    # this is defined earlier
    # log_prefix = '%(remote_ip)s:%(remote_port)s-[%(username)s]'

    def log(self, msg, logfun=None):
        print("log")
        if logfun is None:
            return super(AdaptedFTPHandler, self).log(msg)
        else:
            return super(AdaptedFTPHandler, self).log(msg, logfun)

    def logline(self, msg, logfun=None):
        print("logline")
        return super(AdaptedFTPHandler, self).logline(msg, logfun)

    def logerror(self, msg):
        print("logerror")
        return super(AdaptedFTPHandler, self).logerror(msg)

    def log_exception(self, instance):
        print("log_exception")
        return super(AdaptedFTPHandler, self).log_exception(instance)

    def log_cmd(self, cmd, arg, respcode, respstr):
        print("log_cmd")
        return super(AdaptedFTPHandler, self).log_cmd(cmd, arg, respcode, respstr)

    def log_transfer(self, cmd, filename, receive, completed, elapsed, bytes):
        print("log_transfer")
        return super(AdaptedFTPHandler, self).log_transfer(cmd, filename, receive, completed, elapsed, bytes)

    # --- connection
    def _make_eport(self, ip, port):
        print("_make_eport")
        return super(AdaptedFTPHandler, self)._make_eport(ip, port)

    def _make_epasv(self, extmode=False):
        print("_make_epasv")
        return super(AdaptedFTPHandler, self)._make_epasv(extmode)

    def ftp_PORT(self, line):
        print("ftp_PORT")
        return super(AdaptedFTPHandler, self).ftp_PORT(line)

    def ftp_EPRT(self, line):
        print("ftp_EPRT")
        return super(AdaptedFTPHandler, self).ftp_EPRT(line)

    def ftp_PASV(self, line):
        print("ftp_PASV")
        return super(AdaptedFTPHandler, self).ftp_PASV(line)

    def ftp_EPSV(self, line):
        print("ftp_EPSV")
        return super(AdaptedFTPHandler, self).ftp_EPSV(line)

    def ftp_QUIT(self, line):
        print("ftp_QUIT")
        return super(AdaptedFTPHandler, self).ftp_QUIT(line)

    def ftp_LIST(self, path):
        print("ftp_LIST")
        return super(AdaptedFTPHandler, self).ftp_LIST(path)

    def ftp_NLST(self, path):
       print("ftp_NLST")
       return super(AdaptedFTPHandler, self).ftp_NLST(path)

    # The MLST and MLSD commands are intended to standardize the file and
    # directory information returned by the server-FTP process.  These
    # commands differ from the LIST command in that the format of the
    # replies is strictly defined although extensible.

    def ftp_MLST(self, path):
        print("ftp_MLST")
        return super(AdaptedFTPHandler, self).ftp_MLST(path)

    def ftp_MLSD(self, path):
        print("ftp_MLSD")
        return super(AdaptedFTPHandler, self).ftp_MLSD(path)

    def ftp_STOU(self, line):
        print("ftp_STOU")
        return super(AdaptedFTPHandler, self).ftp_STOU(line)

    def ftp_APPE(self, file):
        print("ftp_APPE")
        return super(AdaptedFTPHandler, self).ftp_APPE(file)

    def ftp_REST(self, line):
        print("ftp_REST")
        return super(AdaptedFTPHandler, self).ftp_REST(line)

    def ftp_ABOR(self, line):
        print("ftp_ABOR")
        return super(AdaptedFTPHandler, self).ftp_ABOR(line)

    def ftp_USER(self, line):
        print("ftp_UER")
        return super(AdaptedFTPHandler, self).ftp_USER(line)

    _auth_failed_timeout = 5

    def ftp_PASS(self, line):
        print("ftp_PASS")
        return super(AdaptedFTPHandler, self).ftp_PASS(line)

    def ftp_REIN(self, line):
        print("ftp_REIN")
        return super(AdaptedFTPHandler, self).ftp_REIN(line)

    def ftp_PWD(self, line):
        print("ftp_PWD")
        return super(AdaptedFTPHandler, self).ftp_PWD(line)

    def ftp_CWD(self, path):
        print("ftp_CWD")
        return super(AdaptedFTPHandler, self).ftp_CWD(path)

    def ftp_CDUP(self, path):
        print("ftp_CDUP")
        return super(AdaptedFTPHandler, self).ftp_CDUP(path)

    def ftp_SIZE(self, path):
        print("ftp_SIZE")
        return super(AdaptedFTPHandler, self).ftp_SIZE(path)

    def ftp_MDTM(self, path):
        print("ftp_MDTM")
        return super(AdaptedFTPHandler, self).ftp_MDTM(path)

    def ftp_MKD(self, path):
        print("ftp_MKD")
        return super(AdaptedFTPHandler, self).ftp_MKD(path)

    def ftp_RMD(self, path):
        print("ftp_RMD")
        return super(AdaptedFTPHandler, self).ftp_RMD(path)

    def ftp_DELE(self, path):
        print("ftp_DELE")
        return super(AdaptedFTPHandler, self).ftp_DELE(path)

    def ftp_RNFR(self, path):
        print("ftp_RNFR")
        return super(AdaptedFTPHandler, self).ftp_RNFR(path)

    def ftp_RNTO(self, path):
        print("ftp_RNTO")
        return super(AdaptedFTPHandler, self).ftp_RNTO(path)

        # --- others
    def ftp_TYPE(self, line):
        print("ftp_TYPE")
        return super(AdaptedFTPHandler, self).ftp_TYPE(line)

    def ftp_STRU(self, line):
        print("ftp_STRU")
        return super(AdaptedFTPHandler, self).ftp_STRU(line)

    def ftp_MODE(self, line):
        print("ftp_MODE")
        return super(AdaptedFTPHandler, self).ftp_MODE(line)

    def ftp_STAT(self, path):
        print("ftp_STAT")
        return super(AdaptedFTPHandler, self).ftp_STAT(path)

    def ftp_FEAT(self, line):
        print("ftp_FEAT")
        return super(AdaptedFTPHandler, self).ftp_FEAT(line)

    def ftp_OPTS(self, line):
        print("ftp_OPTS")
        return super(AdaptedFTPHandler, self).ftp_OPTS(line)

    def ftp_NOOP(self, line):
        print("ftp_NOOP")
        return super(AdaptedFTPHandler, self).ftp_NOOP(line)

    def ftp_SYST(self, line):
        print("ftp_SYST")
        return super(AdaptedFTPHandler, self).ftp_SYST(line)

    def ftp_ALLO(self, line):
        print("ftp_ALLO")
        return super(AdaptedFTPHandler, self).ftp_ALLO(line)

    def ftp_HELP(self, line):
        print("ftp_HELP")
        return super(AdaptedFTPHandler, self).ftp_HELP(line)

    def ftp_SITE_CHMOD(self, path, mode):
        print("ftp_SITE_CHMOD")
        return super(AdaptedFTPHandler, self).ftp_SITE_CHMOD(path, mode)

    def ftp_SITE_HELP(self, line):
        print("ftp_SITE_HELP")
        return super(AdaptedFTPHandler, self).ftp_SITE_HELP(line)

    def ftp_XCUP(self, line):
        print("ftp_XCUP")
        return super(AdaptedFTPHandler, self).ftp_XCUP(line)

    def ftp_XCWD(self, line):
        print("ftp_XCWD")
        return super(AdaptedFTPHandler, self).ftp_XCWD(line)

    def ftp_XMKD(self, line):
        print("ftp_XMKD")
        return super(AdaptedFTPHandler, self).ftp_XMKD(line)

    def ftp_XPWD(self, line):
        print("ftp_XPWD")
        return super(AdaptedFTPHandler, self).ftp_XPWD(line)

    def ftp_XRMD(self, line):
        print("ftp_XRMD")
        return super(AdaptedFTPHandler, self).ftp_XRMD(line)
