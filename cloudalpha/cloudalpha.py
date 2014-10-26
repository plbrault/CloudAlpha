from services.dummy.account import DummyAccount
from services.dropbox.account import DropBoxAccount
from managers.commandline.manager import CommandLineManager

if __name__ == '__main__':

    dummyAccount = DummyAccount("dummy1")
    dropboxAccount = DropBoxAccount("dropbox1")
    manager = CommandLineManager("commandline1")


    manager.file_system_view = dummyAccount.file_system.get_new_view()
    manager.file_system_view = dropboxAccount.file_system.get_new_view()

    dummyAccount.authenticate();
    dropboxAccount.authenticate()

    manager.run()
