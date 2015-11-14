CloudAlpha
==============================================================


The purpose of CloudAlpha is to provide an interface for accessing popular online file hosting services (e.g. Google Drive, Dropbox, etc.) through common file transfer protocols (e.g. FTP, SFTP, etc.). It currently supports Dropbox and FTP, and is designed to be fully extensible. It also provides a dummy storage service account, and a commandline manager, for testing and development purposes.

Copyright (C) 2014 Pier-Luc Brault and Alex Cline


## Licenses

CloudAlpha is licensed under the version 3 of the [GNU Affero General Public License](http://www.gnu.org/licenses/agpl-3.0.en.html). 

The documentation for CloudAlpha is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).


## Documentation

Full documentation for CloudAlpha is included under the "docs" directory of the repository. It includes a Set-Up Guide and a Developer Guide.


## Dependencies

* [Python 3.4](https://www.python.org/)
* [pyftpdlib 1.4.0](https://github.com/giampaolo/pyftpdlib)
* [Dropbox Core API for Python version 2.2](https://www.dropbox.com/developers/core)


## Quick Start

* Install the required dependencies
* Download the latest release of the application
* Get a Dropbox App key and App secret from [Dropbox App Console](https://www.dropbox.com/developers/apps)
* Edit CloudAlpha/config.xml accordingly with the desired configuration and supply it with your App key and App secret
* Run CloudAlpha/cloudalpha.py
