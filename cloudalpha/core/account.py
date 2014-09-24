from abc import ABCMeta, abstractmethod

class Account(object):
    __metaclass__ = ABCMeta
    
    @property
    @abstractmethod
    def account_id(self):
        """Return the unique identifier for the account."""
        pass
    
    @account_id.setter
    @abstractmethod
    def account_id(self, new_id):
        """Set the unique identifier for the account."""
        pass
    
    @property
    @abstractmethod
    def file_system(self):
        """Return the file system object linked to the account.
        
        The return value is an instance of a FileSystem subclass.
        """
        pass
    
    @abstractmethod
    def connect(self):
        """Connect the object to a real file hosting account.
        
        The connection process might require an interaction with the user.
        
        If connection fails, raise ConnectionFailedAccountError.
        """
        pass
    
    @abstractmethod
    def disconnect(self):
        """Disconnect the object from its linked real file hosting account."""
        pass
    
    @abstractmethod
    def __init__(self, account_id, **kwargs):
        """How the initializer of an Account subclass must look like."""
        pass