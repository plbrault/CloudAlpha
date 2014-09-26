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

fileToAdd = "file_to_upload.txt"

file = open(fileToAdd, "rb")

uploaded = False
while not uploaded:
    folder_search = client.search("/", fileToAdd, file_limit=1000, include_deleted=False)
    print("Folder search : ", folder_search)

    if not folder_search:
        response = client.put_file(fileToAdd, file)
        print("File uploaded : ", response)
        uploaded = True
    else:
        print(fileToAdd, "already exists, would you like to update it or rename it? (U/R)")
        update = input().strip().upper()

        if update == "U":
            response = client.put_file(fileToAdd, file, overwrite=True)
            print("File uploaded : ", response)
            uploaded = True
        elif update == "R":
            print("Please enter a new file name : ")
            newName = input().strip()
            fileToAdd = newName + "." + fileToAdd.split(".")[1]
        else:
            print("Invalid input, please try again.")


