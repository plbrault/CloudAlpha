class Manager(object):

    unique_id = None
    file_system_view = None

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
        """The super initializer for Manager subclasses."""
        self.unique_id = unique_id
