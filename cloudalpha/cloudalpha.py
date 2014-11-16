from cloudalpha.services.dropbox.account import DropBoxAccount
from cloudalpha.managers.ftp.manager import FTPManager

if __name__ == '__main__':
    dropboxAccount = DropBoxAccount("dropbox1")
    dropboxAccount.authenticate()

    dropbox_ftp_manager = FTPManager("ftp_dropbox", dropboxAccount.file_system.get_new_view(), 2121, "user", "12345")
    dropbox_ftp_manager.run()
