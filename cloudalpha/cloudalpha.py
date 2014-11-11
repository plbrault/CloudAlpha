from services.dummy.account import DummyAccount
from services.dropbox.account import DropBoxAccount
from managers.commandline.manager import CommandLineManager
from managers.ftp.manager import FtpManager

if __name__ == '__main__':


############################################
######### Dummy + Commandline test #########
############################################

    dummyAccount = DummyAccount("dummy1")
    manager = CommandLineManager("commandline1")
    manager.file_system_view = dummyAccount.file_system.get_new_view()
    dummyAccount.authenticate();
    manager.run()


##############################################
######### Dropbox + Commandline test #########
##############################################

#     dropboxAccount = DropBoxAccount("dropbox1")
#     manager = CommandLineManager("commandline1")
#     manager.file_system_view = dropboxAccount.file_system.get_new_view()
#     dropboxAccount.authenticate()
#     manager.run()


####################################
######### Dummy + FTP test #########
####################################

#     dummyAccount = DummyAccount("dummy1")
#     manager = FtpManager("ftp1")
#     manager.file_system_view = dummyAccount.file_system.get_new_view()
#     dummyAccount.authenticate()
#     manager.run()

######################################
######### Dropbox + FTP test #########
######################################

#     dropboxAccount = DropBoxAccount("dropbox1")
#     manager = FtpManager("ftp1")
#     manager.file_system_view = dropboxAccount.file_system.get_new_view()
#     dropboxAccount.authenticate()
#     manager.run()
