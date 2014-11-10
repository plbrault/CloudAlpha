from core.manager import Manager
from core.exceptions import FileSystemNotSetManagerError

class CommandLineManager(Manager):

    def run(self):
        """Put the manager into action.
        
        If file_system_view is not set, raise FileSystemNotSetManagerError.
        If the operation fails for any other reason, raise StartupFailedManagerError.
        """

        if self.file_system_view == None:
            raise FileSystemNotSetManagerError()

        print("Type help for a list of available commands.")

        terminate = False

        while not terminate:
            try:

                var = input(">" + self.file_system_view.working_dir + ": ").split(" ")
                var = list(filter(None, var))
                if var[0] == "pwd":
                    print(self.file_system_view.working_dir)

                elif var[0] == "cd":
                    if len(var) > 1:
                        self.file_system_view.working_dir = str(var[1])

                elif var[0] == "space_used":
                    print(self.file_system_view.space_used)

                elif var[0] == "free_space":
                    print(self.file_system_view.free_space)

                elif var[0] == "ls":
                    if len(var) == 1:
                        print(self.file_system_view.list_dir())
                    else:
                        print(self.file_system_view.list_dir(var[1]))

                elif var[0] == "meta":
                    if len(var) > 1:
                        print(self.file_system_view.get_metadata(var[1]))
                    else:
                        print(self.file_system_view.get_metadata())

                elif var[0] == "lsm":
                    if len(var) > 1:
                        content_meta = self.file_system_view.get_content_metadata(var[1])
                    else:
                        content_meta = self.file_system_view.get_content_metadata()
                    for meta in content_meta:
                        print(meta)

                elif var[0] == "type":
                    if len(var) > 1:
                        if self.file_system_view.is_dir(str(var[1])):
                            print("directory")
                        elif self.file_system_view.is_file(str(var[1])):
                            print("file")
                    else:
                        raise Exception("missing argument")

                elif var[0] == "size":
                    print(self.file_system_view.get_size(str(var[1])))

                elif var[0] == "created_dt":
                    if len(var) > 1:
                        print(self.file_system_view.get_created_datetime(str(var[1])))
                    else:
                        print(self.file_system_view.get_created_datetime(self.file_system_view.working_dir))

                elif var[0] == "modified_dt":
                    if len(var) > 1:
                        print(self.file_system_view.get_modified_datetime(str(var[1])))
                    else:
                        print(self.file_system_view.get_modified_datetime(self.file_system_view.working_dir))

                elif var[0] == "accessed_dt":
                    if len(var) > 1:
                        print(self.file_system_view.get_accessed_datetime(str(var[1])))
                    else:
                        print(self.file_system_view.get_accessed_datetime(self.file_system_view.working_dir))

                elif var[0] == "mkdir":
                    if len(var) > 1:
                        self.file_system_view.make_dir(str(var[1]))
                    else:
                        raise Exception("missing argument")

                elif var[0] == "mv":
                    if len(var) > 2:
                        self.file_system_view.move(str(var[1]), str(var[2]))
                    else:
                        raise Exception("missing arguments")

                elif var[0] == "cp":
                    if len(var) > 2:
                        self.file_system_view.copy(str(var[1]), str(var[2]))
                    else:
                        raise Exception("missing arguments")

                elif var[0] == "rm":
                    if len(var) > 1:
                        self.file_system_view.delete(str(var[1]))
                    else:
                        raise Exception("missing argument")

                elif var[0] == "download":
                    if len(var) > 2:
                        data = self.file_system_view.read(str(var[1]), 0)
                        local_file = open(str(var[2]), "ab")
                        local_file.write(data)
                        local_file.close()
                    else:
                        raise Exception("missing arguments")

                elif var[0] == "upload":
                    if len(var) > 2:
                        local_file = open(str(var[1]), "rb")
                        data = local_file.read()
                        local_file.close()
                        self.file_system_view.create_new_file(self.unique_id, str(var[2]))
                        self.file_system_view.write_to_new_file(self.unique_id, str(var[2]), data)
                        self.file_system_view.commit_new_file(self.unique_id, str(var[2]))
                    else:
                        raise Exception("missing arguments")

                elif var[0] == "exit":
                    terminate = True;

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
                        + "\n- meta [PATH]"
                        + "\n    prints the metadata of PATH. If PATH is not supplied, uses the current working directory."
                        + "\n- lsm [PATH]"
                        + "\n    prints the metadata of the contents of PATH. If PATH is not supplied, uses the current working directory."
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
                        + "\n    shows the list of available commands"
                        + "\n- exit"
                        + "\n    terminate the Commandline manager")
                else:
                    print("Command \"" + var[0] + "\" not recognized")

            except Exception as e :
                print("An error has occured : ", type(e), e)

    def stop(self):
        """Stop the manager.
        
        If the manager is already stopped, do nothing.
        """
        pass

    def __init__(self, unique_id):
        super(CommandLineManager, self).__init__(unique_id)
