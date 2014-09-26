"""TODO:

Implement a manager that reads and parse commands from the command line, for testing purposes.
"""

from core.manager import Manager

class CommandLineManager(Manager):
    
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