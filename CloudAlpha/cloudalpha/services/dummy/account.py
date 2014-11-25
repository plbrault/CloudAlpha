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

from cloudalpha.account import Account
from cloudalpha.services.dummy.file_system import DummyFileSystem
from cloudalpha.exceptions import AuthenticationFailedAccountError

class DummyAccount(Account):
    """A dummy storage account, for testing purposes."""

    _authenticated = False

    def authenticate(self):
        """Link the object to a real file hosting account. If already done, do nothing.
        
        The association process might require an interaction with the user.
        
        If a required instance attribute is not set, raise MissingAttributeAccountError.
        If a required setting is not set, raise MissingSettingAccountError.
        If the operation fails for any other reason, raise AuthenticationFailedAccountError.
        """
        if not self._authenticated:
            try:
                data = bytearray("# The Zen of Python\nBeautiful is better than ugly.\nExplicit is better than implicit.\nSimple is better than complex."
                        + "\nComplex is better than complicated.\nFlat is better than nested.\nSparse is better than dense.\nReadability counts."
                        + "\nSpecial cases aren't special enough to break the rules.\nAlthough practicality beats purity.\nErrors should never pass"
                        + "silently.\nUnless explicitly silenced.\nIn the face of ambiguity, refuse the temptation to guess."
                        + "\nThere should be one-- and preferably only one --obvious way to do it.\nAlthough that way may not be obvious at first unless you're Dutch."
                        + "\nNow is better than never.\nAlthough never is often better than *right* now.\nIf the implementation is hard to explain, it's a bad idea."
                        + "\nIf the implementation is easy to explain, it may be a good idea.\nNamespaces are one honking great idea -- let's do more of those!", "utf-8")

                new_file_id = self.file_system.create_new_file()
                self.file_system.write_to_new_file(new_file_id, data)
                self.file_system.commit_new_file(new_file_id, "/file1.txt")

                self.file_system.make_dir("/dir1")
                self.file_system.make_dir("/dir2")

                new_file_id = self.file_system.create_new_file()
                self.file_system.write_to_new_file(new_file_id, data)
                self.file_system.commit_new_file(new_file_id, "/dir2/file2.txt")

                self.file_system.make_dir("/dir2/subdir1")

                self.file_system.working_dir = "/"

                self._authenticated = True
            except:
                raise AuthenticationFailedAccountError()

    def __init__(self, unique_id):
        super(DummyAccount, self).__init__(unique_id)
        self.file_system = DummyFileSystem(self)
