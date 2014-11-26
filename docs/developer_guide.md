CloudAlpha Developer Guide
==========================================================================

## Preamble

The purpose of this guide is to help developers to implement new modules in the CloudAlpha project, to improve existing ones, or simply to use the code from CloudAlpha in their own software projects. It contains general information about the source code structure of the project, and on the steps to follow to implement new modules. It does not pretend to be exhaustive or always up-to-date.

## Project Architecture

CloudAlpha is made of *services* and *managers*.

A service is an implementation of a file storage service. It implements an *Account* class, a *FileSystem* class, and optionally, a *Settings* class.

A manager is an implementation of an interface, for instance a FTP interface, for a user to manage the files of a service account. It implements a *Manager* class, and optionally, a *Settings* class.

A FileSystem class inherits from the *cloudalpha.file\_system.FileSystem* abstract class, and implements standard methods to manage the files of the corresponding storage account. Those methods include *make\_dir*, *rename*, *delete*, *read*, etc. A FileSystem instance is referred to by an Account instance, which handles the authentication with the real file storage account.

A Manager class inherits from the *cloudalpha.manager.Manager* abstract class, and implements standard methods to start and stop the manager. It often implements a server, for instance a FTP server. It refers to a unique *FileSystemView* instance, mapped to a FileSystem instance, to which it adds support for a working directory.

A Settings class is a static class that contains updatable settings that are common to all service or manager instances of the same type. For example, the Settings class of the FTP manager defines the FTP server port. It inherits from the *cloudalpha.settings.Settings* abstract class, and implements a *set* method, which can be used to update the values of desired settings.

Service modules are localized under *CloudAlpha/cloudalpha/services* and manager modules are localized under *CloudAlpha/cloudalpha/managers*.

Services and managers can use the *DataStore* singleton to store persistent key-value data. For example, this is useful for storing access tokens for file storage accounts.


