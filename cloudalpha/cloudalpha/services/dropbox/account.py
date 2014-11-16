import webbrowser

from dropbox.client import DropboxOAuth2FlowNoRedirect, DropboxClient

from cloudalpha.account import Account
from cloudalpha.datastore import DataStore
from cloudalpha.exceptions import AuthenticationFailedAccountError
from cloudalpha.services.dropbox.file_system import DropboxFileSystem
from cloudalpha.services.dropbox.settings import Settings


class DropboxAccount(Account):

    _authenticated = False

    def authenticate(self):
        """Link the object to a real file hosting account. If already done, do nothing.
        
        The association process might require an interaction with the user.
        
        If the operation fails, raise AuthenticationFailedAccountError.
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
                raise AuthenticationFailedAccountError()

    def __init__(self, unique_id):
        super(DropboxAccount, self).__init__(unique_id)
        self.file_system = DropboxFileSystem(self)
