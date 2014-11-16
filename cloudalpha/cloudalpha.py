from services.dummy.account import DummyAccount
from services.dropbox.account import DropBoxAccount
from managers.commandline.manager import CommandLineManager
from managers.ftp.manager import FTPManager

if __name__ == '__main__':

    dummyAccount = DummyAccount("dummy1")
    dummyAccount.authenticate()

    dropboxAccount = DropBoxAccount("dropbox1")
    dropboxAccount.authenticate()

    dummy_ftp_manager = FTPManager("ftp_dummy", dummyAccount.file_system.get_new_view(), 2121, "user", "12345")
    dummy_ftp_manager.run()

    dropbox_ftp_manager = FTPManager("ftp_dropbox", dropboxAccount.file_system.get_new_view(), 2122, "user", "12345")
    dropbox_ftp_manager.run()
