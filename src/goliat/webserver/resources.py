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
# $id Goliat/src/goliat/webserver/resourcesloader.py created on 02/04/2010 13:28:44 by damnwidget
'''
Created on 02/04/2010 13:28:44

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary: Web Server resources loader module
@version: 0.1
'''

from twisted.python.filepath import FilePath
from twisted.web import static
import goliat
from goliat.utils.apply import Apply
from goliat.webserver.page import Page
from goliat.module import Module
from goliat.exceptions import ResourcesLoaderException
import os, re
    
class ResourcesLoader:
    """ResourcesLoader Object."""
    _root = None
    _modules = None
    _modules_loaded = False
    _scripts = []     
    _appPath = 'application'
    _scriptPath = 'scripts'    
    _options = {
        'useOrbited'        : False,        
        'resPath'           : {},
        'extjsTheme'        : 'xtheme-gray',
        'goliatTheme'       : 'goliat-gray'
    }    
    
    def __init__(self, root, options={}):
        if root is None or not isinstance(root, Page):
            raise ResourcesLoaderException("The root parameter for ResourcesLoader will be a Goliat Page Instance")
            
        self._root = root
        self._options = Apply(self._options, options)
    
    def Setup(self, module_manager):
        """Setup the loader and load the Goliat Application files"""
        # ===========================
        # Resources
        # ===========================
        
        # Orbited related
        if self._options['useOrbited']:
            # Perform the Orbited imports
            from orbited import logging, config
            import orbited.system
            import orbited.start
            
            # Start logging orbited services
            orbited.start.logger = logging.get_logger('orbited.start')
            # Add static URL to Goliat Page Hierarchy so we can add Stomp JS files on Application         
            self._root.putChild('orbited', static.File(os.path.dirname(orbited.__file__)+os.sep+'static'))
        
        # ExtJS related
        self._root.putChild('extjs', static.File(os.path.dirname(goliat.__file__)+os.sep+'extjs'))        
        
        # Goliat related
        self._root.putChild('goliat', static.File(os.path.dirname(goliat.__file__)+os.sep+'static'))
        
        # Goliat application related
        self._root.putChild('goliat_app', '%s%s%s' % (self._appPath, os.sep, self._scriptPath)) 
        
        # User paths related
        for key, value in self._options['resPath']:            
            if FilePath(value).exists():
                self._root.putChild(key, static.File(value))
        
        # ===========================
        # CSS Styles
        # ===========================
        
        # ExtJS
        self._root.addStyle('<link rel="stylesheet" href="/extjs/resources/css/ext-all.css" type="text/css" />')
        self._root.addStyle('<link rel="stylesheet" href="/extjs/resources/css/%s.css" type="text/css" />' % self._options['extjsTheme'])
        
        # Goliat
        self._root.addStyle('<link rel="stylesheet" href="/goliat/resources/css/%s.css" type="text/css" />' % self._options['goliatTheme'])
        
        # ===========================
        # JavaScript
        # ===========================
        
        # Orbited
        if self._options['useOrbited']:
            self._root.addScript('<script type="text/javascript" characterSet="utf-8" src="/orbited/Orbited.js"></script>')
            self._root.addScript('<script type="text/javascript" characterSet="utf-8" src="/orbited/protocols/stomp.js"></script>')
        
        # ExtJS
        if self._options['debug']:
            self._root.addScript('<script type="text/javascript" characterSet="utf-8" src="/extjs/adapter/ext/ext-base-debug.js"></script>')
            self._root.addScript('<script type="text/javascript" characterSet="utf-8" src="/extjs/ext-all-debug.js"></script>')
        else:
            self._root.addScript('<script type="text/javascript" characterSet="utf-8" src="/extjs/adapter/ext/ext-base.js"></script>')
            self._root.addScript('<script type="text/javascript" characterSet="utf-8" src="/extjs/ext-all.js"></script>')        
        
        # Goliat
        if self._options['debug']:
            self._root.addScript('<script type="text/javascript" characterSet="utf-8" src="/goliat/Goliat-debug.js"></script>')
            self._root.addScript('<script type="text/javascript" characterSet="utf-8">')
            self._root.addScript('    var Goliat_Loader = new Goliat.Loader();')
            self._root.addScript('    Goliat_Loader.loadComponents();')
            self._root.addScript('</script>')
        else:
            self._root.addScript('<script type="text/javascript" characterSet="utf-8" src="/goliat/Goliat.js"></script>')
            #self._root.addScript('<script type="text/javascript" characterSet="utf-8" src="/goliat/Layout-debug.js"></script>')
            #self._root.addScript('<script type="text/javascript" characterSet="utf-8" src="/goliat/LayoutManager-debug.js"></script>')
            #self._root.addScript('<script type="text/javascript" characterSet="utf-8" src="/goliat/Socket-debug.js"></script>')
        
        # ===========================
        # Application main
        # (Defined by User)
        # ===========================
        self._root.addScript('<script type="text/javascript" characterSet="utf-8" src="/scrips/main.js"></script>')
        
        # ===========================
        # Resource Modules
        # ===========================        
        for file in self._exploreApplication():
            module_manager.Register(Module(file))        
    
    def loadScripts(self):
        """Load scripts and fill scripts application list"""
        for file_name in self._exploreApplication(True):
            self._scripts.append(file_name)

    def loadModules(self):
        """Load modules and adds it to the root as childs"""
        for module in self._modules:
            self._root.putChild(module['url_path'], module['module'])

    def _exploreApplication(self, script=False):
        """Explores the module path directory and returns a tuple with filenames."""
        files = os.listdir(self._modulePath)        
        pattern = re.compile('\.py$', re.IGNORECASE) if script == False else re.compile('\.js$', re.IGNORECASE)
        files = filter(pattern.search, files)
        
        return files
            
