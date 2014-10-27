from abc import ABCMeta, abstractmethod

class Manager(object):

    """A base class for implementing a file manager accessible through a specific
    interface, as a network protocol.
    
    Upon its initialization, an instance of a Manager subclass is provided with
    an instance of a FileSystemView subclass, which it is intended to interact with.
    """

    __metaclass__ = ABCMeta

    unique_id = None
    file_system_view = None

    @abstractmethod
    def run(self):
        """Put the manager into action.
        
        If file_system_view is not set, raise FileSystemNotSetManagerError.
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
