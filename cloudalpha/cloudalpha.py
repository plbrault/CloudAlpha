from services.dummy.account import DummyAccount
from managers.commandline.manager import CommandLineManager

if __name__ == '__main__':

    account = DummyAccount("dummy1")
    manager = CommandLineManager("commandline1")

    manager.file_system_view = account.file_system.get_new_view()

    account.authenticate()
    manager.run()
