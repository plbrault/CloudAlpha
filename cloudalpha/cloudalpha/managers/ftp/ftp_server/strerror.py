# ==============================================================================
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
#
#
# This file contains work derived from the source code of the pyftpdlib library,
# covered by the following copyright notice:
#
# Copyright (C) 2007-2014 Giampaolo Rodola' <g.rodola@gmail.com>
#
# ==============================================================================

import pyftpdlib.handlers  # @UnusedImport

""""Redifine pyftpdlib.handlers._sterror function."""
pyftpdlib.handlers._strerror = lambda err: str(err)
