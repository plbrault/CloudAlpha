"""TODO: 

Implement a dummy account, for testing purposes.

Reminder: Account and FileSystem subclasses must be implemented in a thread-safe way.
"""

from core.account import Account
from services.dummy.file_system import DummyFileSystem

class DummyAccount(Account):

    def authenticate(self):
        """Link the object to a real file hosting account.
        
        The association process might require an interaction with the user.
        
        If the operation fails, raise AuthenticationFailedAccountError.
        """
        print("Authenticating")
        tempDir = "/temp/"
        if not self.file_system.is_dir(tempDir):
            print('mkdir')
            self.file_system.make_dir(tempDir);

            filename = '/temp/temp.txt'
            self.file_system.create_new_file(filename, 0)
        pass

    def __init__(self, unique_id):
        super(DummyAccount, self).__init__(unique_id)
        self.file_system = DummyFileSystem()
