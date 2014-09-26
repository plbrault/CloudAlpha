from abc import ABCMeta, abstractmethod

class Account(object):
    
    """A base class for implementing an abstraction of a file hosting service account.
    
    A subclass is defined for each supported file hosting service.
    An instance of an Account subclass provides an instance of the FileSystem
    subclass corresponding to that service.
    
    Account and FileSystem subclasses must be implemented in a thread-safe way.
    """
    
    __metaclass__ = ABCMeta
    
    unique_id = None
    file_system = None
    
    @abstractmethod
    def authenticate(self):
        """Link the object to a real file hosting account.
        
        The association process might require an interaction with the user.
        
        If the operation fails, raise AuthenticationFailedAccountError.
        """
        pass
    
    def __init__(self, unique_id):
        """The super initializer for Account subclasses."""
        self.unique_id = unique_id