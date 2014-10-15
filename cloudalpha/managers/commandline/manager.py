"""TODO:

Implement a manager that reads and parse commands from the command line, for testing purposes.

Commands to implement:
    - pwd
        print the current working directory
    - cd [PATH]
        change the current working directory. Do nothing if PATH is not supplied.
    - space_used
        print the number of bytes used on the file system
    - free_space
        print the number of bytes of free space on the file system
    - ls [PATH]
        list the content of PATH. If PATH is not supplied, use the current working directory.
    - type PATH
        print "dir" if PATH is a directory, and "file" if it is a file
    - size [PATH]
        print the size of PATH, in bytes. If PATH is not supplied, use the current working directory.
    - created_dt [PATH]
        print the created datetime of PATH. If PATH is not supplied, use the current working directory.
    - modified_dt [PATH]
        print the last modified datetime of PATH. If PATH is not supplied, use the current working directory.
    - accessed_dt [PATH]
        print the accessed datetime of PATH. If PATH is not supplied, use the current working directory.
    - mkdir PATH
        create new directory at PATH
    - mv CURRENT-PATH NEW-PATH
        move CURRENT-PATH to NEW-PATH
    - cp PATH COPY_PATH
        copy PATH to COPY_PATH
    - rm PATH
        delete the file or directory at PATH
    - download REMOTE-PATH LOCAL-PATH
        download a file from REMOTE-PATH to the local hard drive
    - upload LOCAL-PATH REMOTE-PATH
        upload a file from the local hard drive to REMOTE-PATH
    - help
        show the list of available commands

The commands are implemented using self.file_system, which corresponds to a FileSystem subclass instance.
"""

from core.manager import Manager
import os

class CommandLineManager(Manager):

    def run(self):
        """Put the manager into action.
        
        If file_system is not set, raise FileSystemNotSetManagerError.
        If the operation fails for any other reason, raise StartupFailedManagerError.
        """
        commands = ["pwd", "cd", "space_used", "free_space", "ls", "type", "size", "created_dt", "modified_dt", "accessed_dt", "mkdir", "mv", "cp", "rm", "download", "upload", "help"]

        while 1 is 1:

            var = input(">" + self.file_system.working_dir + ":").split(" ")
            if var[0] == commands[0]:
                print(self.file_system.working_dir)
            elif var[0] == commands[1]:
                if len(var) == 1:
                    print("Error: missing PATH")
                elif not len(var) == 2:
                    print("Error: Too many parameters")
                else:

                    self.file_system.working_dir = str(var[1])

    def stop(self):
        """Stop the manager.
        
        If the manager is already stopped, do nothing.
        """
        pass

    def __init__(self, unique_id):
        super(CommandLineManager, self).__init__(unique_id)
