"""TODO: 

Implement a dummy account, for testing purposes.

Reminder: Account and FileSystem subclasses must be implemented in a thread-safe way.
"""

from core.account import Account
from services.dummy.file_system import DummyFileSystem

class DummyAccount(Account):

    def authenticate(self):
        pass

    def __init__(self, unique_id):
        super(DummyAccount, self).__init__(unique_id)
        self.file_system = DummyFileSystem()
