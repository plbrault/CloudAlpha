# CloudAlpha #

The purpose of CloudAlpha is to provide an interface for accessing popular online file hosting services (e.g. Google Drive, Dropbox, etc.) through common file transfer protocols (e.g. FTP, SFTP, etc.).
It currently supports Dropbox and FTP, and is designed to be fully extensible. It also provides a dummy storage service account, and a commandline manager, for testing and development purposes.

Copyright (C) 2014 Pier-Luc Brault and Alex Cline

## Status ##
Alpha

## Dependencies ##
* [Python 3.4 or later](https://www.python.org/)
* [pyftpdlib 1.4.0](https://github.com/giampaolo/pyftpdlib)
* [Dropbox Core API for Python](https://www.dropbox.com/developers/core)

## Current Known Issues ##
* Running multiple FTP server instances simultaneously does not work properly.

## How to use
* Install the required dependencies
* Download the latest realease of the application
* Supply cloudalpha/cloudalpha/services/dropbox/settings.json with a valid Dropbox App key and App secret
* Edit cloudalpha/config.xml accordingly with the desired configuration
* Run cloudalpha/cloudalpha.py