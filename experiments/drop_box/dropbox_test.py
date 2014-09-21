from drop_box.settings import Settings
from dropbox.client import DropboxOAuth2FlowNoRedirect, DropboxClient

flow = DropboxOAuth2FlowNoRedirect(Settings.app_key, Settings.app_secret)


authorize_url = flow.start()

authenticated = False
while not authenticated:
    print('1. Go to: ' + authorize_url)
    print('2. Click "Allow" (you might have to log in first)')
    print('3. Copy the authorization code.')
    print('4. Enter the authorization code :')
    
    code = input().strip()
    print()
    
    try:        
        access_token, user_id = flow.finish(code)
        print("Authentication succeeded")
        authenticated = True
    except:
        print("Authentication failed. Try again :")

client = DropboxClient(access_token)

file = open("file_to_upload.txt", "rb")
response = client.put_file("file_to_upload.txt", file)
print("File uploaded : ", response)