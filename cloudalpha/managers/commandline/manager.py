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
                    print(self.file_system.list_dir())
                else:
                    print(self.file_system.list_dir(var[1]))

            elif var[0] == "type":
                if len(var) > 1:
                    if self.file_system.is_dir(str(var[1])):
                        print("directory")
                    elif self.file_system.is_file(str(var[1])):
                        print("file")

            elif var[0] == "size":
                print(self.file_system.get_size(str(var[1])))

            elif var[0] == "created_dt":
                if len(var) > 1:
                    print(self.file_system.get_created_datetime(str(var[1])))
                else:
                    print(self.file_system.get_created_datetime(self.file_system.working_dir))

            elif var[0] == "modified_dt":
                if len(var) > 1:
                    print(self.file_system.get_modified_datetime(str(var[1])))
                else:
                    print(self.file_system.get_modified_datetime(self.file_system.working_dir))

            elif var[0] == "accessed_dt":
                if len(var) > 1:
                    print(self.file_system.get_accessed_datetime(str(var[1])))
                else:
                    print(self.file_system.get_accessed_datetime(self.file_system.working_dir))

            elif var[0] == "mkdir":
                if len(var) > 1:
                    self.file_system.make_dir(str(var[1]))

            elif var[0] == "mv":
                if len(var) > 2:
                    self.file_system.move(str(var[1]), str(var[2]))

            elif var[0] == "cp":
                if len(var) > 2:
                    self.file_system.copy(str(var[1]), str(var[2]))

            elif var[0] == "rm":
                if len(var) > 1:
                    self.file_system.delete(str(var[1]))

            elif var[0] == "download":
                if len(var) == 3:
                    data = self.file_system.read(str(var[1]), 0)
                    local_file = open(str(var[2]), "ab")
                    local_file.write(data)
                    local_file.close()

            elif var[0] == "upload":
                if len(var) == 3:
                    local_file = open(str(var[1]), "rb")
                    data = local_file.read()
                    local_file.close()
                    self.file_system.create_new_file(str(var[2]), len(data))
                    self.file_system.write_to_new_file(str(var[2]), data)
                    self.file_system.commit_new_file(str(var[2]))

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
