import json
import webbrowser

from dropbox.client import DropboxOAuth2FlowNoRedirect, DropboxClient

from core.account import Account
from core.exceptions import AuthenticationFailedAccountError
from services.dropbox.file_system import DropBoxFileSystem
from services.dropbox.settings import Settings

class DropBoxAccount(Account):

    _authenticated = False

    def authenticate(self):
        """Link the object to a real file hosting account. If already done, do nothing.
        
        The association process might require an interaction with the user.
        
        If the operation fails, raise AuthenticationFailedAccountError.
        """

        flow = DropboxOAuth2FlowNoRedirect(Settings.app_key, Settings.app_secret)

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

        self.file_system._client = DropboxClient(access_token)

    def __init__(self, unique_id):
        super(DropBoxAccount, self).__init__(unique_id)
        self.file_system = DropBoxFileSystem(self)
