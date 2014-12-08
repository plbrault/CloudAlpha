CloudAlpha Set-Up Guide
==============================================================


## Preamble

The purpose of this guide is to supply the information needed to set-up and use CloudAlpha. It does not pretend to be exhaustive, as it assumes that you have advanced computer knowledge, including installing a Python interpreter with libraries, and editting XML files. It also does not pretend to be always up-to-date.

Copyright (C) 2014 Pier-Luc Brault and Alex Cline

[http://github.com/plbrault/CloudAlpha](http://github.com/plbrault/CloudAlpha)


## Licenses

This document is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).

CloudAlpha is licensed under the version 3 of the [GNU Affero General Public License](http://www.gnu.org/licenses/agpl-3.0.en.html).


## Contents

* [Dependencies](#dependencies)
* [Installation](#installation)
* [Configuration](#configuration)
* [Using the Application](#using-the-application)


## Dependencies

### Python 3.4

CloudAlpha has been developed and tested with the CPython implementation of [Python](https://www.python.org/) 3.4. It has not been tested with other Python 3.x releases, neither has it been tested with other Python implementations, but it might be compatible.

### Module-Specific Dependencies

#### FTP

The FTP module requires the version 1.4 of the [pyftpdlib](https://github.com/giampaolo/pyftpdlib) library. It might be compatible with other versions, but it has not been tested.

#### Dropbox

The Dropbox module requires the version 2.2 of the [Dropbox Core API](https://www.dropbox.com/developers/core). It might be compatible with other versions, but it has not been tested.


## Installation

To install CloudAlpha, get the latest release at [https://github.com/plbrault/CloudAlpha/releases](https://github.com/plbrault/CloudAlpha/releases), then extract the archive to the desired installation directory.


## Configuration

To configure CloudAlpha, you have to edit the `CloudAlpha/config.xml` file. By default, this file should be formatted as below:

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

It is an XML file divided in two main sections: `services` and `managers`. Services correspond to file hosting services, while managers correspond to the interfaces (usually protocols) used to access them.

Configuring CloudAlpha corresponds to configuring manager-service pairs, by specifying which service accounts you want the application to access, and by which interfaces.

To add a service account, you have to add the corresponding `accountInstance` entry in the `instances` subsection of the `services` section.

To add an interface for a service account, you have to add the corresponding `managerInstance` under the `instances` subsection of the `managers` section.

The `uniqueID` attributes must always contain values that are unique to their respective entries. They will be used to identify the corresponding services and managers.

You might also have to add entries to the `globalSettings` subsections if the services and managers you configure require so.

### Module-Specific Instructions

#### Dropbox

To use Dropbox with CloudAlpha, you first have to get Dropbox API keys by following these steps :
	
* Open the [Dropbox App Console](https://www.dropbox.com/developers/apps) in a web browser
* Log in with your Dropbox account
* Click on *Create app*
* Select *Dropbox API app*
* Select *Files and datastores*
* Select *No - My app needs access to files already on Dropbox.*
* Select *All file types*
* Enter any desired name for App name (ex: yourName.CloudAlpha)
* Click on *Create app*

You now have access to your *App key* and *App secret* under the *Settings* tab. Copy these into the `globalSettings` subsection of the `services` section of the configuration file, as below:
 
	    <services>
	        <globalSettings>
	            <service name="dropbox">
	                <setting name="app_key">INSERT APP KEY HERE</setting>
	                <setting name="app_secret">INSERT APP SECRET HERE</setting>
	            </service>
	        </globalSettings>

Next, setup the desired Dropbox accounts under the `instances` subsection, as below:

	        <instances>
	            <accountInstance uniqueID="dropbox1" service="dropbox"/>        
	        </instances>

The `uniqueID` attribute will be used to refer to the account in the `managers` section.

#### FTP

To use a service account through FTP, you first have to set the network port that the FTP server will be listening to, in the `globalSettings` subsection of the `managers` section of the configuration file, as below:

	    <managers>
	        <globalSettings>
	            <manager name="ftp">
	                <setting name="ftp_server_port">2121</setting>
	            </manager>
	        </globalSettings>

Next, setup the instances as below:

	        <instances>
	            <managerInstance uniqueID="ftp-dropbox1" type="ftp" account="dropbox1">
	                <parameter name="ftp_username">user</parameter>
	                <parameter name="ftp_password">12345</parameter>
	            </managerInstance>          
	        </instances>

The `account` attribute contains the `uniqueID` of the service account linked to the instance. The `ftp_username` and `ftp_password` parameters specify the username and password used to connect to the account through FTP.


## Using the Application

Start the application by running `CloudAlpha/cloudalpha.py` with a compatible Python interpreter (see [Dependencies](#dependencies)). For example:

	cd CloudAlpha
	python cloudalpha.py

### Required File Permissions

The application should be executed with the necessary permissions to read from and write to a file named `datastore.db` in the `CloudAlpha` directory. If this file does not already exist, it will be created automatically.

### Module-Specific Instructions

#### Dropbox

The first time you use the application with a given `uniqueID` for a Dropbox instance, it will open a web page on Dropbox with your default browser, asking you to authorize the application to access your Dropbox account. It will give you an authorization code that you will have to copy into the
application prompt.

#### FTP

Use your favorite FTP client to access FTP instances defined in your configuration file. Use the address of the host running CloudAlpha (or `localhost` if your client is on the same machine) with the port, username and password defined in the configuration file. 