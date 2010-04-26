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
# $id Goliat/src/goliat/modulemgr.py created on 03/04/2010 00:13:39 by damnwidget
'''
Created on 03/04/2010 00:13:39

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary: Modules Manager
@version: 0.1
'''
from datetime import datetime

class ModuleManager(object):
    """The module manager keeps a pool of active modules."""

    _modules=list()

    def __init__(self):
        """Initialize the module manager."""
        super(ModuleManager, self).__init__()

    def register(self, module):
        """Add a new module to the pool."""
        self._modules.append(module)
        module.load()
        now=datetime.now()
        print '{0} [-] Module {1} registered'.format(
            now.strftime("%Y-%m-%d %H:%M:%S+0")+str(now.microsecond)[:3],
            module.get_module())

    def lenght(self):
        """Returns the module pool lenght."""
        return len(self._modules)

    def get_modules(self):
        """Return the pool."""
        return self._modules

