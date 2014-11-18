# =============================================================================
# Copyright (C) 2014 Pier-Luc Brault and Alex Cline
#
# This file is part of CloudAlpha.
#
# CloudAlpha is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CloudAlpha is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with CloudAlpha.  If not, see <http://www.gnu.org/licenses/>.
#
# http://github.com/plbrault/cloudalpha
# =============================================================================

import webbrowser

from dropbox.client import DropboxOAuth2FlowNoRedirect, DropboxClient

from cloudalpha.account import Account
from cloudalpha.datastore import DataStore
from cloudalpha.exceptions import AuthenticationFailedAccountError
from cloudalpha.services.dropbox.file_system import DropboxFileSystem
from cloudalpha.services.dropbox.settings import Settings


class DropboxAccount(Account):
    """This class allows the interaction with a Dropbox account."""

    _authenticated = False

    def authenticate(self):
        """Link the object to a real file hosting account. If already done, do nothing.
        
        The association process might require an interaction with the user.
        
        If a required attribute is not set, raise MissingAttributeAccountError.
        If the operation fails for any other reason, raise AuthenticationFailedAccountError.
        """

        flow = DropboxOAuth2FlowNoRedirect(Settings.app_key, Settings.app_secret)

        authorize_url = flow.start()

        if not self._authenticated:
            try:
                access_token = DataStore().get_value(self.unique_id, "access_token")

                if access_token == None:
                    webbrowser.open(authorize_url)
                    print('Allow access and enter the authorization code :')
                    code = input().strip()
                    print()
                    access_token = flow.finish(code)[0]
                    DataStore().set_value(self.unique_id, "access_token", access_token)

                self.file_system._client = DropboxClient(access_token)
                print("Authentication succeeded")
            except:
                raise AuthenticationFailedAccountError

    def __init__(self, unique_id):
        """DropboxAccount initializer"""
        super(DropboxAccount, self).__init__(unique_id)
        self.file_system = DropboxFileSystem(self)
