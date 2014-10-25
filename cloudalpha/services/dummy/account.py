from core.account import Account
from services.dummy.file_system import DummyFileSystem
from core.exceptions import AuthenticationFailedAccountError

class DummyAccount(Account):

    _authenticated = False

    def authenticate(self):
        """Link the object to a real file hosting account. If already done, do nothing.
        
        The association process might require an interaction with the user.
        
        If the operation fails, raise AuthenticationFailedAccountError.
        """
        if not self.authenticated:
            try:
                data = bytearray("# The Zen of Python\nBeautiful is better than ugly.\nExplicit is better than implicit.\nSimple is better than complex."
                        + "\nComplex is better than complicated.\nFlat is better than nested.\nSparse is better than dense.\nReadability counts."
                        + "\nSpecial cases aren't special enough to break the rules.\nAlthough practicality beats purity.\nErrors should never pass"
                        + "silently.\nUnless explicitly silenced.\nIn the face of ambiguity, refuse the temptation to guess."
                        + "\nThere should be one-- and preferably only one --obvious way to do it.\nAlthough that way may not be obvious at first unless you're Dutch."
                        + "\nNow is better than never.\nAlthough never is often better than *right* now.\nIf the implementation is hard to explain, it's a bad idea."
                        + "\nIf the implementation is easy to explain, it may be a good idea.\nNamespaces are one honking great idea -- let's do more of those!", "utf-8")

                self.file_system.create_new_file("account_authenticate", "/file1.txt", 860)
                self.file_system.write_to_new_file("account_authenticate", "/file1.txt", data)
                self.file_system.commit_new_file("account_authenticate", "/file1.txt")

                self.file_system.make_dir("/dir1")
                self.file_system.make_dir("/dir2")

                self.file_system.create_new_file("account_authenticate", "/dir2/file2.txt", 860)
                self.file_system.write_to_new_file("account_authenticate", "/dir2/file2.txt", data)
                self.file_system.commit_new_file("account_authenticate", "/dir2/file2.txt")

                self.file_system.make_dir("/dir2/subdir1")

                self.file_system.working_dir = "/"

                self.authenticated = True
            except:
                raise AuthenticationFailedAccountError()

    def __init__(self, unique_id):
        super(DummyAccount, self).__init__(unique_id)
        self.file_system = DummyFileSystem(self)
