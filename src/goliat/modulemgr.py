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
# $id /home/damnwidget/Aptana Studio Workspace/Goliat/src/goliat/modulemgr.py created on 03/04/2010 00:13:39 by damnwidget
'''
Created on 03/04/2010 00:13:39

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: damnwidget
@contact: oscar.campos@open-phoenix.com
@summary:
@version: 0.1
'''
class ModuleManager:
    _modules = list()
    _modulePath = None
    
    def __init__(self, module_path):
        self._modulePath = module_path
            
    def Register(self, module):
        """Add a new module to self"""
        self._modules.append(module)
        module.Load(self._modulePath)    
    
    def lenght(self):
        """Returns the self lenght"""
        return len(self._modules)    
    
    def getModules(self):
        return self._modules    
    
    