from abc import ABCMeta, abstractmethod

class Manager(object):
    __metaclass__ = ABCMeta
    
    @property
    @abstractmethod
    def manager_id(self):
        """Return the unique identifier for the manager."""
        pass
    
    @manager_id.setter
    @abstractmethod
    def manager_id(self, manager_id):
        """Set the unique identifier for the manager."""
        pass
    
    @property
    @abstractmethod
    def port(self):
        """Return the port number used by the manager."""
        pass
    
    @port.setter
    @abstractmethod
    def port(self, port):
        """Set the port number used by the manager."""
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
        """Put the manager into action."""
        pass
    
    @abstractmethod
    def stop(self):
        """Stop the manager."""
        pass
    
    @abstractmethod
    def __init__(self, manager_id, **kwargs):
        """How the initializer of a Manager subclass must look like."""
        pass    