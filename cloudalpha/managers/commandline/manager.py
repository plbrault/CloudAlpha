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

        while True:

            var = input(">" + self.file_system.working_dir + ":").split(" ")
            var = list(filter(None, var))
            if var[0] == "pwd":
                print(self.file_system.working_dir)

            elif var[0] == "cd":
                if len(var) > 1:
                    self.file_system.working_dir = str(var[1])

            elif var[0] == "space_used":
                print(self.file_system.space_used)

            elif var[0] == "free_space":
                print(self.file_system.free_space)

            elif var[0] == "ls":
                if len(var) == 1:
                    print(self.file_system.list_dir(None))
                else:
                    print(self.file_system.list_dir(var[1]))

            elif var[0] == "type":
                if len(var) > 1:
                    if self.file_system.is_dir(str(var[1])):
                        print("directory")
                    elif self.file_system.is_file(str(var[1])):
                        print("file")

            elif var[0] == "size":
                pass

            elif var[0] == "created_dt":
                pass

            elif var[0] == "modified_dt":
                pass

            elif var[0] == "accessed_dt":
                pass

            elif var[0] == "mkdir":
                if len(var) > 1:
                    self.file_system.make_dir(str(var[1]))

            elif var[0] == "mv":
                pass

            elif var[0] == "cp":
                pass

            elif var[0] == "rm":
                if len(var) > 1:
                    self.file_system.delete(str(var[1]))

            elif var[0] == "download":
                pass

            elif var[0] == "upload":
                pass

            elif var[0] == "help":
                print("- pwd"
                    + "\n    prints the current working directory"
                    + "\n- cd [PATH]"
                    + "\n    changes the current working directory."
                    + "\n- space_used"
                    + "\n    prints the number of bytes used on the file system"
                    + "\n- free_space"
                    + "\n    prints the number of bytes of free space on the file system"
                    + "\n- ls [PATH]"
                    + "\n    lists the contents of PATH. If PATH is not supplied, uses the current working directory."
                    + "\n- type [PATH]"
                    + "\n    prints \"dir\" if PATH is a directory, and \"file\" if it is a file"
                    + "\n- size [PATH]"
                    + "\n    prints the size of PATH, in bytes. If PATH is not supplied, uses the current working directory."
                    + "\n- created_dt [PATH]"
                    + "\n    prints the created datetime of PATH. If PATH is not supplied, uses the current working directory."
                    + "\n- modified_dt [PATH]"
                    + "\n    prints the last modified datetime of PATH. If PATH is not supplied, uses the current working directory."
                    + "\n- accessed_dt [PATH]"
                    + "\n    prints the accessed datetime of PATH. If PATH is not supplied, uses the current working directory."
                    + "\n- mkdir [PATH]"
                    + "\n    creates new directory at PATH"
                    + "\n- mv [CURRENT-PATH] [NEW-PATH]"
                    + "\n    moves CURRENT-PATH to NEW-PATH"
                    + "\n- cp [PATH] [COPY_PATH]"
                    + "\n    copies PATH to COPY_PATH"
                    + "\n- rm [PATH]"
                    + "\n    deletes the file or directory at PATH"
                    + "\n- download [REMOTE-PATH] [LOCAL-PATH]"
                    + "\n    downloads a file from REMOTE-PATH to the local hard drive"
                    + "\n- upload [LOCAL-PATH] [REMOTE-PATH]"
                    + "\n    uploads a file from the local hard drive to REMOTE-PATH"
                    + "\n- help"
                    + "\n    shows the list of available commands")
            else:
                print("Command \"" + var[0] + "\" not recognised")

    def stop(self):
        """Stop the manager.
        
        If the manager is already stopped, do nothing.
        """
        pass

    def __init__(self, unique_id):
        super(CommandLineManager, self).__init__(unique_id)
