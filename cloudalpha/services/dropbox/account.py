from core.account import Account
from services.dropbox.file_system import DropBoxFileSystem
from core.exceptions import AuthenticationFailedAccountError
from dropbox.client import DropboxOAuth2FlowNoRedirect, DropboxClient

import json
import webbrowser

class DropBoxAccount(Account):

    _authenticated = False

    def authenticate(self):
        """Link the object to a real file hosting account. If already done, do nothing.
        
        The association process might require an interaction with the user.
        
        If the operation fails, raise AuthenticationFailedAccountError.
        """

        _file_data = open("services/dropbox/settings.json").read()
        _json_obj = json.loads(_file_data)

        flow = DropboxOAuth2FlowNoRedirect(_json_obj["app_key"], _json_obj["app_secret"])


        authorize_url = flow.start()

        if not self._authenticated:

            webbrowser.open(authorize_url)
            print('Allow access and enter the authorization code :')

            code = input().strip()
            print()

            try:
                access_token, user_id = flow.finish(code)
                print("Authentication succeeded")
                self._authenticated = True
            except:
                raise AuthenticationFailedAccountError()

        client = DropboxClient(access_token)

    def __init__(self, unique_id):
        super(DropBoxAccount, self).__init__(unique_id)
        self.file_system = DropBoxFileSystem(self)
