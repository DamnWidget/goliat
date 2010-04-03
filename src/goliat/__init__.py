# -*- coding: utf-8 -*-
##
# Goliat: The Twisted and ExtJS Web Framework
# Copyright (C) 2010 Open Phoenix IT
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
##
# $id Goliat/src/goliat/__init__.py created on 02/04/2010 13:15:10 by damnwidget
'''
Created on 02/04/2010 13:15:10

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: damnwidget
@contact: oscar.campos@open-phoenix.com
@summary: Goliat is a Web Framework that integrates well known Python technologies with
the hope that it will help to develop RAD Web Applications.
Goliat uses the following Technologies:
Orbited for COMET
Twisted for Internet Framework
Storm as ORM
ExtJS as GUI System
Goliat as been developed by Open Phoenix IT S.Coop.And. http://www.open-phoenix.com 
@version: 0.1
'''

# Ensure the user is running the version of python we require.
import sys
if not hasattr(sys, "version_info") or sys.version_info < (2,4):
    raise RuntimeError("Goliat requires Python 2.4 or later.")
del sys

# setup version
from _version import version
__version__ = version.short()
