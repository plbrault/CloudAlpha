from services.dummy.account import DummyAccount
from services.dropbox.account import DropBoxAccount
from managers.commandline.manager import CommandLineManager
from managers.ftp.manager import FTPManager

if __name__ == '__main__':
    dropboxAccount = DropBoxAccount("dropbox1")
    dropboxAccount.authenticate()

    dropbox_ftp_manager = FTPManager("ftp_dropbox", dropboxAccount.file_system.get_new_view(), 2121, "user", "12345")
    dropbox_ftp_manager.run()
