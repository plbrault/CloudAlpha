from abc import ABCMeta, abstractmethod

class Manager(object):
    
    """A base class for implementing a file manager accessible through a specific
    interface, as a network protocol.
    
    Upon its initialization, an instance of a Manager subclass is provided with
    an instance of a FileSystem subclass, which it is intended to interact with.
    """
    
    __metaclass__ = ABCMeta
    
    @property
    @abstractmethod
    def unique_id(self):
        """Return the unique identifier for the manager."""
        pass
    
    @unique_id.setter
    @abstractmethod
    def unique_id(self, unique_id):
        """Set the unique identifier for the manager."""
        pass
    
    @property
    @abstractmethod
    def file_system(self):
        """Return the file system which the manager interacts with.
        
        The return value is an instance of a FileSystem subclass.
        """
        pass
    
    @file_system.setter
    @abstractmethod
    def file_system(self, file_system):
        """Set the file system which the manager interacts with.
        
        The given value must be an instance of a FileSystem subclass."""
        pass
    
    @abstractmethod
    def run(self):
        """Put the manager into action.
        
        If file_system is not set, raise FileSystemNotSetManagerError.
        If the operation fails for any other reason, raise StartupFailedManagerError.
        """
        pass
    
    @abstractmethod
    def stop(self):
        """Stop the manager.
        
        If the manager is already stopped, do nothing.
        """
        pass
    
    def __init__(self, unique_id):
        """The super initializer for Manager subclasses."""
        self.unique_id = unique_id   