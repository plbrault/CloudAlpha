from drop_box.settings import Settings
from dropbox.client import DropboxOAuth2FlowNoRedirect

flow = DropboxOAuth2FlowNoRedirect(Settings.app_key, Settings.app_secret)