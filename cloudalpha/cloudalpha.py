from services.dummy.account import DummyAccount
from managers.commandline.manager import CommandLineManager

if __name__ == '__main__':

    account = DummyAccount("dummy1")
    manager = CommandLineManager("commandline1")

    manager.file_system = account.file_system

    account.authenticate()


    data = ("# The Zen of Python\nBeautiful is better than ugly.\nExplicit is better than implicit.\nSimple is better than complex."
            + "\nComplex is better than complicated.\nFlat is better than nested.\nSparse is better than dense.\nReadability counts."
            + "\nSpecial cases aren't special enough to break the rules.\nAlthough practicality beats purity.\nErrors should never pass"
            + "silently.\nUnless explicitly silenced.\nIn the face of ambiguity, refuse the temptation to guess."
            + "\nThere should be one-- and preferably only one --obvious way to do it.\nAlthough that way may not be obvious at first unless you're Dutch."
            + "\nNow is better than never.\nAlthough never is often better than *right* now.\nIf the implementation is hard to explain, it's a bad idea."
            + "\nIf the implementation is easy to explain, it may be a good idea.\nNamespaces are one honking great idea -- let's do more of those!")

    account.file_system.create_new_file("file1.txt", 1000)
    account.file_system.write_to_new_file("file1.txt", data)

    account.file_system.make_dir("fun")
    account.file_system.working_dir = "fun"
    print(account.file_system.list_dir())
    print(account.file_system.working_dir)

    account.file_system.make_dir("brine")
    account.file_system.working_dir = "brine"
    print(account.file_system.list_dir())
    print(account.file_system.working_dir)

    account.file_system.create_new_file("file2.txt", 1000)
    account.file_system.write_to_new_file("file2.txt", data)

    account.file_system.working_dir = "/"
    print(account.file_system.list_dir())
    print(account.file_system.working_dir)

    account.file_system.working_dir = "/fun"
    print(account.file_system.list_dir())
    print(account.file_system.working_dir)

    manager.run()
