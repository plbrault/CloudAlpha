CloudAlpha Developer Guide
==========================================================================


## Preamble

The purpose of this guide is to help developers to implement new modules in the CloudAlpha project, to improve existing ones, or simply to use the code from CloudAlpha in their own software projects. It contains general information about the source code structure of the project, and on the steps to follow to implement new modules. It does not pretend to be exhaustive or always up-to-date, and also assumes that you are familiar with the Python programming language.

Copyright (C) 2014 Pier-Luc Brault and Alex Cline


## License

This document is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).


## Contents

* [Project Architecture](#project-architecture)
* [Useful to Know](#useful-to-know)
* [Implementing a Service](#implementing-a-service)
* [Implementing a Manager](#implementing-a-manager)
* [Class Reference](#class-reference)


## Project Architecture

### Services and Managers

CloudAlpha is made of *services* and *managers*.

A service is an implementation of a file storage service. It implements an `Account` class, a `FileSystem` class, and optionally, a `Settings` class.

A manager is an implementation of an interface, for instance a FTP interface, for a user to manage the files of a service account. It implements a `Manager` class, and optionally, a `Settings` class.

Service modules are localized under `CloudAlpha/cloudalpha/services` and manager modules are localized under `CloudAlpha/cloudalpha/managers`.

### Classes

A `FileSystem` class inherits from the `cloudalpha.file_system.FileSystem` abstract class, and implements standard methods to manage the files of the corresponding storage account. Those methods include `make_dir`, `rename`, `delete`, `read`, etc. A `FileSystem` instance is referred to by an `Account` instance, which handles the authentication with the real file storage account.

A `Manager` class inherits from the `cloudalpha.manager.Manager` abstract class, and implements standard methods to start and stop the manager. It often implements a server, for instance a FTP server. It refers to a unique `FileSystemView` instance. A `FileSystemView` instance is mapped to a `FileSystem` instance, to which it adds the support for a working directory.

A `Settings` class is a static class that contains updatable settings that are common to all service or manager instances of the same type. For example, the `Settings` class of the FTP manager defines the FTP server port. It inherits from the `cloudalpha.settings.Settings` abstract class, and implements a `set` method, which can be used to update the values of desired settings.

Services and managers can use the `DataStore` singleton to store persistent key-value data. For example, this is useful for storing access tokens for file storage accounts.

### Configurator

CloudAlpha also implements a `configurator`, which uses reflection to instantiate and configure service and manager instances based on the content of an XML file. The main module then authenticates generated `Account` instances and starts generated `Manager` instances.

### Main Module

The "main" is defined in `CloudAlpha/cloudalpha.py`. It executes the configurator with `CloudAlpha/config.xml`, then authenticates the generated accounts and starts the generated managers.

### File Structure Overview

This is an overview of the file structure of CloudAlpha:

	CloudAlpha
	|-- cloudalpha
	|	|-- managers
	|	|	|-- commandline
	|	|	|	|-- commandline_thread.py
	|	|	|	|-- manager.py
	|	|	|-- ftp
	|	|	|	|-- ftp_server
	|	|	|	|-- manager.py
	|	|	|	|-- settings.py
	|	|-- services
	|	|	|-- dropbox
	|	|	|	|-- account.py
	|	|	|	|-- file_system.py
	|	|	|	|-- settings.py
	|	|	|-- dummy
	|	|	|	|-- account.py
	|	|	|	|-- file_system.py
	|	|-- account.py
	|	|-- datastore.py
	|	|-- exceptions.py
	|	|-- file_metadata.py
	|	|-- file_system_view.py
	|	|-- file_system.py
	|	|-- manager.py
	|	|-- settings.py
	|-- configurator
	|	|-- configurator.py
	|	|-- configurator.xsd
	|-- cloudalpha.py
	|-- config.xml
	|-- datastore.db


## Useful to Know

### Unique Identifiers

Each `Account` and `Manager` instance has a `unique_id` attribute which is set at creation time. As implied by its name, the `unique_id` attribute must be given a value unique to its owner.

### How the Configurator Works

A typical config.xml file looks like this:

	<CloudAlphaConfig>
	    <services>
	        <globalSettings>
	            <service name="dropbox">
	                <setting name="app_key">INSERT APP_KEY HERE</setting>
	                <setting name="app_secret">INSERT APP_SECRET HERE</setting>
	            </service>
	        </globalSettings>
	        <instances>
	            <accountInstance uniqueID="dropbox1" service="dropbox"/>        
	        </instances>
	    </services>
	    <managers>
	        <globalSettings>
	            <manager name="ftp">
	                <setting name="ftp_server_port">2121</setting>
	            </manager>
	        </globalSettings>
	        <instances>
	            <managerInstance uniqueID="ftp-dropbox1" type="ftp" account="dropbox1">
	                <parameter name="ftp_username">user</parameter>
	                <parameter name="ftp_password">12345</parameter>
	            </managerInstance>          
	        </instances> 
	    </managers>
	</CloudAlphaConfig>

As you can see, it is divided in two main sections: services and managers. The `globalSettings` subsections define settings that are applicable to all instances of specified services or managers, and the `instances` subsections define instances of services and managers to create.

The configurator uses reflection to apply the settings and create the instances. For example, it will search for a module named "dropbox" under `cloudalpha.services`, and will look for a settings module under this package, then for a subclass of `cloudalpha.settings.Settings` inside that module. It will finally use the `set` method of that class to apply the specified settings.

The same happens with instances: to create the FTP instance, the configurator will look for a subclass of `Manager` in `cloudalpha.managers.ftp.manager`, then it will call its constructor with the specified `ftp_username` and `ftp_password` parameters.

### How to Use the DataStore

The `Datastore` is a singleton specified in the `cloudalpha.datastore` module. It allows the services and managers to store persistent key-value pairs that will be available in the future to instances with the same `unique_id` values.

The following code snippet shows how to use it:

	from cloudalpha.account import Account
	from cloudalpha.datastore import DataStore

	class ExampleAccount(Account):
		def authenticate(self):
			access_token = DataStore().get_value(self.unique_id, "access_token")
			if not access_token:
				access_token = ask_user_for_token()
				DataStore().set_value(self.unique_id, "access_token", access_token)

### Dummy Service and Commandline Manager

A dummy service and a commandline manager are implemented for development and testing purposes. It might be more practical to use the dummy service instead of a real one when implementing a new manager, and to use the commandline manager instead of a real one when implementing a new service. To use them, all you have to do is to add corresponding instances to your configuration file.

### Development Configuration

During development, you will probably have to make changes to `config.xml` that you will not want to commit, which is rather impractical. There is a simple solution to this: instead of modifying `config.xml`, add a new `config.dev.xml` file that will contain your testing configuration. When this file is present, it is passed to the configurator instead of the default configuration file. Also, it is included in the `.gitignore` file of the project.


## Implementing a Service

This section assumes that you have read the preceding sections of this document.

To implement a new service, create a new directory with the name of that service under `CloudAlpha/cloudalpha/services` and add an empty `__init__.py` file in it.

The new directory must contain an `account.py` file, a `file_system.py` file, and optionnaly, a `settings.py` file.

The `account.py` file will implement a subclass of the `cloudalpha.account.Account` abstract class.

The `file_system.py` file will implement a subclass of the `cloudalpha.file_system.FileSystem` abstract class.

The `settings.py` file is needed only if your service needs global settings to be set by the configurator. In this case, it will implement a subclass of the `cloudalpha.settings.Settings` abstract class.

All these subclasses must implement all the abstract methods of their respective base classes, and must also conform to the requirements specified by the docstrings of the latter, which can be found in the [Class Reference](#class-reference) section of this document. Furthermore, the `__init__` methods of the subclasses must take the same arguments as the initializers of their respective base classes, and every `__init__` method should call its super `__init__` method.

All exception types mentioned by the specifications of the base classes are defined in the `cloudalpha.exceptions` module.


## Implementing a Manager

This section assumes that you have read the preceding sections of this document.

To implement a new manager, create a new directory with the name of that manager under `CloudAlpha/cloudalpha/manager` and add an empty `__init__.py` file in it.

The new directory must contain a `manager.py` file, and optionnaly, a `settings.py` file.

The `manager.py` file will implement a subclass of the `cloudalpha.manager.Manager` abstract class, with all the methods defined in it.

The `settings.py` file is needed only if your manager needs global settings to be set by the configurator. In this case, it will implement a subclass of the `cloudalpha.settings.Settings` abstract class.

All these subclasses must implement all the abstract methods of their respective base classes, and must also conform to the requirements specified by the docstrings of the latter, which can be found in the [Class Reference](#class-reference) section of this document. Furthermore, the `__init__` methods of the subclasses must take the same arguments as the initializers of their respective base classes, and every `__init__` method should call its super `__init__` method.

All exception types mentioned by the specifications of the base classes are defined in the `cloudalpha.exceptions` module.


## Class Reference

### `cloudalpha.account.Account`

    A base class for implementing an abstraction of a file hosting service account.
    
    A subclass is defined for each supported file hosting service.
    An instance of an Account subclass provides an instance of the FileSystem
    subclass corresponding to that service.
    
    Methods defined here:
    
    __init__(self, unique_id, *args, **kwargs)
        The super initializer for Account subclasses.
        
        Subclass initializers must take the same first 2 arguments, 
        and all subsequent arguments must be optional and must accept 
        string values.
        
        If an argument cannot be parsed to the proper type,
        raise ArgumentParsingAccountError.
    
    authenticate(self)
        Link the object to a real file hosting account. If already done, do nothing.
        
        The association process might require an interaction with the user.
        
        If a required instance attribute is not set, raise MissingAttributeAccountError.
        If a required setting is not set, raise MissingSettingAccountError.
        If the operation fails for any other reason, raise AuthenticationFailedAccountError.
    
    ----------------------------------------------------------------------
    Data descriptors defined here:
    
    __dict__
        dictionary for instance variables (if defined)
    
    __weakref__
        list of weak references to the object (if defined)
    
    ----------------------------------------------------------------------
    Data and other attributes defined here:
    
    __metaclass__ = <class 'abc.ABCMeta'>
        Metaclass for defining Abstract Base Classes (ABCs).
        
        Use this metaclass to create an ABC.  An ABC can be subclassed
        directly, and then acts as a mix-in class.  You can also register
        unrelated concrete classes (even built-in classes) and unrelated
        ABCs as 'virtual subclasses' -- these and their descendants will
        be considered subclasses of the registering ABC by the built-in
        issubclass() function, but the registering ABC won't show up in
        their MRO (Method Resolution Order) nor will method
        implementations defined by the registering ABC be callable (not
        even via super()).
    
    file_system = None
    
    unique_id = None

### `cloudalpha.datastore.DataStore`

    A singleton allowing the storage and retrieving of persistent key-value pairs.
    
    Methods defined here:
    
    get_value(self, unique_id, key)
        Retrieve the value corresponding to the specified unique_id and key. If such a value does not exist, return None.
    
    set_value(self, unique_id, key, value)
        Store the given value associated to the specified unique_id and key.
    
    ----------------------------------------------------------------------
    Static methods defined here:
    
    __new__(cls, *args, **kwargs)
        Return the singleton instance.
    
    ----------------------------------------------------------------------
    Data descriptors defined here:
    
    __dict__
        dictionary for instance variables (if defined)
    
    __weakref__
        list of weak references to the object (if defined)

### `cloudalpha.file_metadata.FileMetadata`

    Class representing the metadata of a file.
    
    Methods defined here:
    
    __init__(self, path='', is_dir=False, size=0, created_datetime=None, accessed_datetime=None, modified_datetime=None)
        FileMetadata initializer
    
    __str__(self)
        Return a string representing the object.
    
    ----------------------------------------------------------------------
    Data descriptors defined here:
    
    __dict__
        dictionary for instance variables (if defined)
    
    __weakref__
        list of weak references to the object (if defined)
    
    name
        Return the short name of the file, excluding its location.
    
    ----------------------------------------------------------------------
    Data and other attributes defined here:
    
    accessed_datetime = None
    
    created_datetime = None
    
    is_dir = False
    
    modified_datetime = None
    
    path = ''
    
    size = 0

### `cloudalpha.file_system.FileSystem`

    A base class for implementing an abstraction of a file system, that may in fact
    be an adapter for managing the content of a file hosting service account.
    
    A subclass of FileSystem is defined for each supported file hosting service.
    An instance of a FileSystem subclass is linked to a single
    instance of an Account subclass.
    
    FileSystem subclasses must be implemented in a thread-safe way.
    
    Methods defined here:
    
    __init__(self, account)
        The super initializer for FileSystem subclasses.
    
    commit_new_file(self, new_file_id, path)
        Commit the file corresponding to new_file_id and store it at the location represented by path.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.     
        
        If there is no uncommited file corresponding to new_file_id, raise IDNotFoundFileSystemError.
        If the parent path is invalid, raise InvalidPathFileSystemError. 
        If the parent path does not correspond to a directory, raise InvalidTargetFileSystemError.
        If the given path points to an existing file, overwrite it.
        If the given path corresponds to an existing directory, raise InvalidTargetFileSystemError.  
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    copy(self, path, copy_path)
        Copy a file or directory from path to copy_path.
        
        new_path includes the name of the copied file or directory.
        The paths must be absolute POSIX pathnames, with "/" representing the root of the file system.
        
        If path is invalid, raise InvalidPathFileSystemError.
        If copy_path corresponds to an existing file or directory, raise AlreadyExistsFileSystemError.
        If new_path is a subpath of old_path , raise ForbiddenOperationFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    create_new_file(self)
        Create an empty file that will be populated by successive calls to write_to_new_file. Return a unique
        ID that will be needed to perform write_to_new_file, commit_new_file and flush_new_file calls.
        
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    delete(self, path)
        Delete the file or directory corresponding to the given path.
        
        If the given path corresponds to a directory that is not empty, all its files and subdirectories
        must be deleted first.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    exists(self, path)
        Return True if the given path points to an existing file or directory, excluding uncommitted files.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    flush_new_file(self, new_file_id)
        Delete an uncommitted file.
        
        If there is no uncommited file corresponding to new_file_id, raise IDNotFoundFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    get_accessed_datetime(self, path)
        Return the date and time of the last time the given file or directory was accessed.
        If not available, return the date and time of the last modification.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        The return value is a datetime object.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    get_content_metadata(self, path)
        Return an iterable of FileMetadata objects representing the contents of the directory corresponding to the given path.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the given path does not point to a directory, raise InvalidTargetFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    get_created_datetime(self, path)
        Return the date and time of creation of the file or directory corresponding to the given path.
        If not available, return the date and time of the last modification.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        The return value is a datetime object.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    get_metadata(self, path)
        Return a FileMetadata object representing the file or directory corresponding to the given path.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    get_modified_datetime(self, path)
        Return the date and time of the last modification to the file or directory corresponding to the given path.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        The return value is a datetime object.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    get_new_view(self)
        Return a new FileSystemView linked to the current FileSystem subclass instance.
    
    get_size(self, path)
        Return the size, in bytes, of the file corresponding to the given path.
        If the path points to a directory, return 0.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    is_dir(self, path)
        Return a boolean value indicating if the given path corresponds to a directory.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    is_file(self, path)
        Return a boolean value indicating if the given path corresponds to a file.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    list_dir(self, path)
        Return the content of the specified directory.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
                
        The return value is a list of file and folder names. It does not contain references to the current
        or parent directory (e.g. "." or "..").
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the given path does not correspond to a directory, raise InvalidTargetFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    make_dir(self, path)
        Creates a new directory corresponding to the given path.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If the parent path is invalid, raise InvalidPathFileSystemError.
        If the given path corresponds to an existing file or directory, raise AlreadyExistsFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    move(self, old_path, new_path)
        Move and/or rename a file or directory from old_path to new_path.
        
        new_path includes the new name of the file or directory.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        If old_path is invalid, raise InvalidPathFileSystemError.
        If new_path corresponds to an existing file or directory, raise AlreadyExistsFileSystemError.
        If new_path is a subpath of old_path , raise ForbiddenOperationFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    read(self, path, start_byte, num_bytes=None)
        Read the number of bytes corresponding to num_bytes from the file corresponding to the given path,
        beginning at start_byte.
        
        If start_byte is greater than the size of the file, return an empty iterable.
        
        If num_bytes is not specified, read all remaining bytes of the file.
        
        The given path must be an absolute POSIX pathname, with "/" representing the root of the file system.
        
        The return value is an iterable of bytes.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the given path corresponds to a directory, raise InvalidTargetFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    write_to_new_file(self, new_file_id, data)
        Append the given data to the uncommitted file corresponding to new_file_id.
        
        The data must be an iterable of bytes.
        
        If there is no uncommited file corresponding to new_file_id, raise IDNotFoundFileSystemError.
        If there is not enough free space to store the new data, raise InsufficientSpaceFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    ----------------------------------------------------------------------
    Data descriptors defined here:
    
    __dict__
        dictionary for instance variables (if defined)
    
    __weakref__
        list of weak references to the object (if defined)
    
    free_space
        Return the free space remaining on the file system, in bytes.
        
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    lock
        Return the Lock object for the current instance.
    
    space_used
        Return the number of bytes used on the file system.
        
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    ----------------------------------------------------------------------
    Data and other attributes defined here:
    
    __metaclass__ = <class 'abc.ABCMeta'>
        Metaclass for defining Abstract Base Classes (ABCs).
        
        Use this metaclass to create an ABC.  An ABC can be subclassed
        directly, and then acts as a mix-in class.  You can also register
        unrelated concrete classes (even built-in classes) and unrelated
        ABCs as 'virtual subclasses' -- these and their descendants will
        be considered subclasses of the registering ABC by the built-in
        issubclass() function, but the registering ABC won't show up in
        their MRO (Method Resolution Order) nor will method
        implementations defined by the registering ABC be callable (not
        even via super()).

### `cloudalpha.file_system_view.FileSystemView`

    This class is mapped to a FileSystem subclass instance and redirects
    all method calls to it. It implements the support of a working directory.
    
    Methods defined here:
    
    __init__(self, file_system)
        Create a new FileSystemView instance linked to the given FileSystem subclass instance.
    
    commit_new_file(self, new_file_id, path)
        Commit the file corresponding to new_file_id and store it at the location represented by path.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory. 
        
        If there is no uncommited file corresponding to new_file_id, raise IDNotFoundFileSystemError.
        If the parent path is invalid, raise InvalidPathFileSystemError. 
        If the parent path does not correspond to a directory, raise InvalidTargetFileSystemError.
        If the given path points to an existing file, overwrite it.
        If the given path corresponds to an existing directory, raise InvalidTargetFileSystemError.  
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    copy(self, path, copy_path)
        Copy a file or directory from path to copy_path.
        
        new_path includes the name of the copied file or directory.
        The paths must be POSIX pathnames, with "/" representing the root of the file system.
        They may be absolute, or relative to the current working directory.
        
        If path is invalid, raise InvalidPathFileSystemError.
        If copy_path corresponds to an existing file or directory, raise AlreadyExistsFileSystemError.
        If new_path is a subpath of old_path , raise ForbiddenOperationFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    create_new_file(self)
        Create an empty file that will be populated by successive calls to write_to_new_file. Return a unique
        ID that will be needed to perform write_to_new_file, commit_new_file and flush_new_file calls.
        
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    delete(self, path)
        Delete the file or directory corresponding to the given path.
        
        If the given path corresponds to a directory that is not empty, all its files and subdirectories
        must be deleted first.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    exists(self, path)
        Return True if the given path points to an existing file or directory, excluding uncommitted files.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    flush_new_file(self, new_file_id)
        Delete an uncommitted file.
        
        If there is no uncommited file corresponding to new_file_id, raise IDNotFoundFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    get_abs_path(self, path)
        Return the absolute path corresponding to the given relative path.
    
    get_accessed_datetime(self, path)
        Return the date and time of the last time the given file or directory was accessed.
        If not available, return the date and time of the last modification.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        The return value is a datetime object.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    get_content_metadata(self, path=None)
        Return an iterable of FileMetadata objects representing the contents of the directory corresponding to the given path.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the given path does not point to a directory, raise InvalidTargetFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    get_created_datetime(self, path)
        Return the date and time of creation of the file or directory corresponding to the given path.
        If not available, return the date and time of the last modification.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        The return value is a datetime object.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    get_metadata(self, path=None)
        Return a FileMetadata object representing the file or directory corresponding to the given path.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        If path is None, use the current working directory.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    get_modified_datetime(self, path)
        Return the date and time of the last modification to the file or directory corresponding to the given path.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        The return value is a datetime object.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    get_size(self, path)
        Return the size, in bytes, of the file corresponding to the given path.
        If the path points to a directory, return 0.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    is_dir(self, path)
        Return a boolean value indicating if the given path corresponds to a directory.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    is_file(self, path)
        Return a boolean value indicating if the given path corresponds to a file.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    list_dir(self, path=None)
        Return the content of the specified directory. If no directory is specified, return the content of the current working directory.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
                
        The return value is a list of file and folder names. It does not contain references to the current
        or parent directory (e.g. "." or "..").
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the given path does not correspond to a directory, raise InvalidTargetFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    make_dir(self, path)
        Creates a new directory corresponding to the given path.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        If the parent path is invalid, raise InvalidPathFileSystemError.
        If the given path corresponds to an existing file or directory, raise AlreadyExistsFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    move(self, old_path, new_path)
        Move and/or rename a file or directory from old_path to new_path.
        
        new_path includes the new name of the file or directory.
        
        The paths must be POSIX pathnames, with "/" representing the root of the file system.
        They may be absolute, or relative to the current working directory.
        
        If old_path is invalid, raise InvalidPathFileSystemError.
        If new_path corresponds to an existing file or directory, raise AlreadyExistsFileSystemError.
        If new_path is a subpath of old_path , raise ForbiddenOperationFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    read(self, path, start_byte, num_bytes=None)
        Read the number of bytes corresponding to num_bytes from the file corresponding to the given path,
        beginning at start_byte.
        
        If start_byte is greater than the size of the file, return an empty iterable.
        
        If num_bytes is not specified, read all remaining bytes of the file.
        
        The given path must be a POSIX pathname, with "/" representing the root of the file system.
        It may be absolute, or relative to the current working directory.
        
        The return value is an iterable of bytes.
        
        If the given path is invalid, raise InvalidPathFileSystemError.
        If the given path corresponds to a directory, raise InvalidTargetFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    write_to_new_file(self, new_file_id, data)
        Append the given data to the uncommitted file corresponding to new_file_id.
        
        The data must be an iterable of bytes.
        
        If there is no uncommited file corresponding to new_file_id, raise IDNotFoundFileSystemError.
        If there is not enough free space to store the new data, raise InsufficientSpaceFileSystemError.
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    ----------------------------------------------------------------------
    Data descriptors defined here:
    
    __dict__
        dictionary for instance variables (if defined)
    
    __weakref__
        list of weak references to the object (if defined)
    
    free_space
        Return the free space remaining on the file system, in bytes.
        
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    lock
    
    space_used
        Return the number of bytes used on the file system.
        
        If the real file system is inaccessible, raise AccessFailedFileSystemError.
    
    working_dir
        Return the path of the current working directory.
        
        The return value is a POSIX pathname, with "/" representing the root of the file system.

### `cloudalpha.manager.Manager`

    A base class for implementing a file manager accessible through a specific
    interface, as a network protocol.
    
    Upon its initialization, an instance of a Manager subclass is provided with
    an instance of a FileSystemView subclass, which it is intended to interact with.
    
    Methods defined here:
    
    __init__(self, unique_id, file_system_view=None, *args, **kwargs)
        The super initializer for Manager subclasses.
        
        Subclass initializers must take the same first 3 arguments, 
        and all subsequent arguments must be optional and must accept 
        string values.
        
        If an argument cannot be parsed to the proper type,
        raise ArgumentParsingManagerError.
    
    run(self)
        Put the manager into action, in a new thread. If already done, do nothing.
        
        If a required instance attribute is not set, raise MissingAttributeManagerError.
        If a required setting is not set, raise MissingSettingManagerError.
        If the operation fails for any other reason, raise StartupFailedManagerError.
    
    stop(self)
        Stop the manager.
        
        If the manager is already stopped, do nothing.
    
    ----------------------------------------------------------------------
    Data descriptors defined here:
    
    __dict__
        dictionary for instance variables (if defined)
    
    __weakref__
        list of weak references to the object (if defined)
    
    ----------------------------------------------------------------------
    Data and other attributes defined here:
    
    __metaclass__ = <class 'abc.ABCMeta'>
        Metaclass for defining Abstract Base Classes (ABCs).
        
        Use this metaclass to create an ABC.  An ABC can be subclassed
        directly, and then acts as a mix-in class.  You can also register
        unrelated concrete classes (even built-in classes) and unrelated
        ABCs as 'virtual subclasses' -- these and their descendants will
        be considered subclasses of the registering ABC by the built-in
        issubclass() function, but the registering ABC won't show up in
        their MRO (Method Resolution Order) nor will method
        implementations defined by the registering ABC be callable (not
        even via super()).
    
    file_system_view = None
    
    unique_id = None

### `cloudalpha.settings.Settings`

    A base class for implementing global settings in services and managers.
    
    Class methods defined here:
    
    set(name, value) from builtins.type
        Update the value of the setting corresponding to name.
        
        If there is no setting corresponding to name, raise InvalidNameSettingError.
        
        value can be of type string. It will be converted to the proper type before 
        it is stored. In case of parsing failure, raise ValueParsingSettingError.
    
    ----------------------------------------------------------------------
    Data descriptors defined here:
    
    __dict__
        dictionary for instance variables (if defined)
    
    __weakref__
        list of weak references to the object (if defined)
    
    ----------------------------------------------------------------------
    Data and other attributes defined here:
    
    __metaclass__ = <class 'abc.ABCMeta'>
        Metaclass for defining Abstract Base Classes (ABCs).
        
        Use this metaclass to create an ABC.  An ABC can be subclassed
        directly, and then acts as a mix-in class.  You can also register
        unrelated concrete classes (even built-in classes) and unrelated
        ABCs as 'virtual subclasses' -- these and their descendants will
        be considered subclasses of the registering ABC by the built-in
        issubclass() function, but the registering ABC won't show up in
        their MRO (Method Resolution Order) nor will method
        implementations defined by the registering ABC be callable (not
        even via super()).