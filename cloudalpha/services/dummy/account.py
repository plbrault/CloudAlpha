"""TODO: 

Implement a dummy account, for testing purposes.
"""

from core.account import Account

class DummyAccount(Account):
        
    @property
    def unique_id(self):
        """Return the unique identifier for the account."""
        pass
    
    @unique_id.setter
    def unique_id(self, new_id):
        """Set the unique identifier for the account."""
        pass
    
    @property
    def file_system(self):
        """Return the file system object linked to the account.
        
        The return value is an instance of a FileSystem subclass.
        """
        pass
    
    def authenticate(self):
        """Link the object to a real file hosting account.
        
        The association process might require an interaction with the user.
        
        If the operation fails, raise AuthenticationFailedAccountError.
        """
        pass
    
    def __init__(self, unique_id):
        super(DummyAccount, self).__init__(unique_id)