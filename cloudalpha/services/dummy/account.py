"""TODO: 

Implement a dummy account, for testing purposes.

Reminder: Account and FileSystem subclasses must be implemented in a thread-safe way.
"""

from core.account import Account
from services.dummy.file_system import DummyFileSystem

class DummyAccount(Account):

    def authenticate(self):
        data = ("# The Zen of Python\nBeautiful is better than ugly.\nExplicit is better than implicit.\nSimple is better than complex."
                + "\nComplex is better than complicated.\nFlat is better than nested.\nSparse is better than dense.\nReadability counts."
                + "\nSpecial cases aren't special enough to break the rules.\nAlthough practicality beats purity.\nErrors should never pass"
                + "silently.\nUnless explicitly silenced.\nIn the face of ambiguity, refuse the temptation to guess."
                + "\nThere should be one-- and preferably only one --obvious way to do it.\nAlthough that way may not be obvious at first unless you're Dutch."
                + "\nNow is better than never.\nAlthough never is often better than *right* now.\nIf the implementation is hard to explain, it's a bad idea."
                + "\nIf the implementation is easy to explain, it may be a good idea.\nNamespaces are one honking great idea -- let's do more of those!")

        self.file_system.create_new_file("file1.txt", 1000)
        self.file_system.write_to_new_file("file1.txt", data)

        self.file_system.make_dir("fun")

        self.file_system.make_dir("brine")

        self.file_system.create_new_file("file2.txt", 1000)
        self.file_system.write_to_new_file("file2.txt", data)

        self.file_system.working_dir = "/"

    def __init__(self, unique_id):
        super(DummyAccount, self).__init__(unique_id)
        self.file_system = DummyFileSystem()
