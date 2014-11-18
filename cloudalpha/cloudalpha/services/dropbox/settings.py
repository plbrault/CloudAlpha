import os.path
import json

class Settings:
    """This class retrieves the information from settings.json, or from
    settings.dev.json if it exists.
    """

    if os.path.isfile("cloudalpha/services/dropbox/settings.dev.json"):
        _file_data = open("cloudalpha/services/dropbox/settings.dev.json").read()
        _json_obj = json.loads(_file_data)
    else:
        _file_data = open("cloudalpha/services/dropbox/settings.json").read()
        _json_obj = json.loads(_file_data)

    app_key = _json_obj["app_key"]
    app_secret = _json_obj["app_secret"]
