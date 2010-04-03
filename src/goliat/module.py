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
# $id Goliat/src/goliat/modules.py created on 02/04/2010 23:33:11 by damnwidget
from codegen.codegen import globals
'''
Created on 02/04/2010 23:33:11

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary: Module Object 
@version: 0.1
'''
class Module:    
    _urlPath = None
    _object = None
    _name = None
    _loaded = False
    
    def __init__(self, name):
        self._name = name    
    
    def getUrlPath(self):
        return self._urlPath
        
    def setUrlPath(self, url):
        self._urlPath = url
    
    def getModule(self):
        return self._object    
    
    def getName(self):
        return self._name
    
    def setName(self, name):
        self._name = name
    
    def Load(self, module_path):
        if self._loaded:
            return
        
        _moduleName = "%s.%s" % ( module_path, self._name )
        _objList = [self._name.capitalize()]
        _tempModule = __import__(_moduleName, globals(), locals(), _objList) 
        self._object = getattr(_tempModule, _objList[0])
        self._urlPath = self._object.getRegisterPath()
        self._loaded = True             
    
    def isLoaded(self):
        return self._loaded        
        