# CloudAlpha

The purpose of CloudAlpha is to provide an interface for accessing popular online file hosting services (e.g. Google Drive, Dropbox, etc.) through common file transfer protocols (e.g. FTP, SFTP, etc.).
It currently supports Dropbox and FTP, and is designed to be fully extensible. It also provides a dummy storage service account, and a commandline manager, for testing and development purposes.

Copyright (C) 2014 Pier-Luc Brault and Alex Cline

## License

CloudAlpha is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CloudAlpha is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with CloudAlpha.  If not, see [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).

## Status
Alpha

## Dependencies
* [Python 3.4 or later](https://www.python.org/)
* [pyftpdlib 1.4.0](https://github.com/giampaolo/pyftpdlib)
* [Dropbox Core API for Python](https://www.dropbox.com/developers/core)

## How to use
* Install the required dependencies
* Download the latest realease of the application
* Get a Dropbox App key and App secret from [Dropbox App Console](https://www.dropbox.com/developers/apps)
* Edit CloudAlpha/config.xml accordingly with the desired configuration and supply it with your App key and App secret
* Run CloudAlpha/cloudalpha.py