"""TODO:

Implement a manager that reads and parse commands from the command line, for testing purposes.
"""

from core.manager import Manager

class CommandLineManager(Manager):
    
    @property
    def unique_id(self):
        """Return the unique identifier for the manager."""
        pass
    
    @unique_id.setter
    def unique_id(self, unique_id):
        """Set the unique identifier for the manager."""
        pass
    
    @property
    def file_system(self):
        """Return the file system which the manager interacts with.
        
        The return value is an instance of a FileSystem subclass.
        """
        pass
    
    @file_system.setter
    def file_system(self, file_system):
        """Set the file system which the manager interacts with.
        
        The given value must be an instance of a FileSystem subclass."""
        pass
    
    def run(self):
        """Put the manager into action.
        
        If file_system is not set, raise FileSystemNotSetManagerError.
        If the operation fails for any other reason, raise StartupFailedManagerError.
        """
        pass
    
    def stop(self):
        """Stop the manager.
        
        If the manager is already stopped, do nothing.
        """
        pass
    
    def __init__(self, unique_id):
        super(CommandLineManager, self).__init__(unique_id)