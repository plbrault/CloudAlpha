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

from configurator.configurator import Configurator, ConfiguratorError
import os

if __name__ == '__main__':
    """Generate the accounts and managers specified in config.xml, and launch them."""
    try:
        if os.path.exists("config.dev.xml"):
            configurator = Configurator("config.dev.xml")
        else:
            configurator = Configurator("config.xml")
        for account in configurator.get_accounts():
            account.authenticate()
        for manager in configurator.get_managers():
            manager.run()
    except ConfiguratorError as e:
        print(e)
