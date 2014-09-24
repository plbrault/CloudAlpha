from abc import ABCMeta, abstractmethod

class Account(object):
    
    """A base class for implementing an abstraction of a file hosting service account.
    
    A subclass is defined for each supported file hosting service.
    An instance of an Account subclass provides an instance of the FileSystem
    subclass corresponding to that service.
    
    Account and FileSystem subclasses must be implemented in a thread-safe way.
    """
    
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
    def authenticate(self):
        """Link the object to a real file hosting account.
        
        The association process might require an interaction with the user.
        
        If the operation fails, raise AuthenticationFailedAccountError.
        """
        pass
    
    def __init__(self, account_id):
        """The super initializer for Account subclasses."""
        self.account_id = account_id