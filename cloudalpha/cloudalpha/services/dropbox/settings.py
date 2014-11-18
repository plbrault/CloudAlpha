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
