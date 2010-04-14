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
from compiler.pycodegen import gen
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
from twisted.web import static, resource
from storm.base import Storm
from goliat.module import Module
from goliat.database import Database, Generator, DatabaseException
import goliat
import os, re
    
class ResourcesLoader(object):
    """ResourcesLoader Object."""
    _root = None
    _modules = None
    _modules_loaded = False
    _scripts = []     
    _appPath = 'application'
    _scriptPath = 'scripts'    
    _options = dict()        
    
    def __init__(self, root, options=dict()):           
        self._root = root
        self._options = options
        self._loadScripts()
    
    def Setup(self, module_manager):
        """Setup the loader and load the Goliat Application files"""
        # ===========================
        # Resources
        # ===========================
        
        # Orbited related
        if self._options['orbited']:
            import orbited # For get the __file__            
            # Add static URL to Goliat Page Hierarchy so we can add Stomp JS files on Application         
            self._root.putChild('static', static.File(os.path.dirname(orbited.__file__)+'/static'))
        
        # ExtJS related
        self._root.putChild('extjs', static.File(os.path.dirname(goliat.__file__)+'/static/extjs'))        
        
        # Goliat related
        self._root.putChild('goliat', static.File(os.path.dirname(goliat.__file__)+'/static'))
        
        # Goliat application related
        self._root.putChild('ui', static.File('{0}/{1}'.format( self._appPath, self._scriptPath )))         
        self._root.putChild('js', static.File('web/js'))
        self._root.putChild('media', static.File('web/media'))
        self._root.putChild('css', static.File('web/css'))
        
        # User paths related
        for key, value in self._options['respath']:            
            if FilePath(value).exists():
                self._root.putChild(key, static.File(value))
        
        # ===========================
        # CSS Styles
        # ===========================
        
        # ExtJS
        self._root.addStyle('<link rel="stylesheet" href="/extjs/resources/css/ext-all.css" type="text/css" />')
        self._root.addStyle('<link rel="stylesheet" href="/extjs/resources/css/{0}.css" type="text/css" />'.format( self._options['extjsTheme'] ))
        
        # Goliat
        self._root.addStyle('<link rel="stylesheet" href="/goliat/resources/css/{0}.css" type="text/css" />'.format( self._options['goliatTheme'] ))
        
        # ===========================
        # JavaScript
        # ===========================
        
        # Orbited
        if self._options['orbited']:
            self._root.addScript('<script type="text/javascript" characterSet="utf-8" src="/static/Orbited.js"></script>')
            self._root.addScript('<script type="text/javascript" characterSet="utf-8" src="/static/protocols/stomp/stomp.js"></script>')
        
        # ExtJS
        if self._options['debug']:
            self._root.addScript('<script type="text/javascript" characterSet="utf-8" src="/extjs/adapter/ext/ext-base-debug.js"></script>')
            self._root.addScript('<script type="text/javascript" characterSet="utf-8" src="/extjs/ext-all-debug.js"></script>')
        else:
            self._root.addScript('<script type="text/javascript" characterSet="utf-8" src="/extjs/adapter/ext/ext-base.js"></script>')
            self._root.addScript('<script type="text/javascript" characterSet="utf-8" src="/extjs/ext-all.js"></script>')        
        
        # Goliat
        if self._options['debug']:            
            self._root.addScript('<script type="text/javascript" characterSet="utf-8" src="/goliat/js/Loader.js"></script>')            
            self._root.addScript('<script type="text/javascript" characterSet="utf-8">')
            self._root.addScript('    var Goliat_Loader = new Goliat.Loader();')
            self._root.addScript('    Goliat_Loader.loadComponents();')
            self._root.addScript('</script>')
                       
        else:
            self._root.addScript('<script type="text/javascript" characterSet="utf-8" src="/goliat/js/goliat-min.js"></script>')
            #self._root.addScript('<script type="text/javascript" characterSet="utf-8" src="/goliat/Layout-debug.js"></script>')
            #self._root.addScript('<script type="text/javascript" characterSet="utf-8" src="/goliat/LayoutManager-debug.js"></script>')
            #self._root.addScript('<script type="text/javascript" characterSet="utf-8" src="/goliat/Socket-debug.js"></script>')
        self._root.addScript('<script type="text/javascript" characterSet="utf-8" src="/goliat/js/locale/goliat-lang-{0}.js"></script>'.format( self._options['locale'] ))        
        
        # ===========================
        # Application main
        # (Coded by User)
        # ===========================
        self._root.addScript('<script type="text/javascript" characterSet="utf-8" src="/js/main.js"></script>')
        
        # ===========================
        # Application UI
        # ===========================
        for uiScript in self._scripts:
            self._root.addScript('<script type="text/javascript" characterSet="utf-8" src="/ui/{0}"></script>'.format( uiScript ))
        
        # ===========================
        # Resource Modules
        # ===========================        
        for file in self._exploreApplication():
            module_manager.Register(Module(file))
        
        # Append Resources to the root object        
        for module in module_manager.getModules():
            self._root.putChild(module.getUrlPath(), module.getModule())       
            
    
    def _loadScripts(self):
        """Load scripts and fill scripts application list"""
        for file_name in self._exploreApplication(True):
            self._scripts.append(file_name)    

    def _exploreApplication(self, script=False):
        """Explores the module path directory and returns a tuple with filenames."""
        try:
            files = os.listdir('application')        
            pattern = re.compile('[^_?]\.py$', re.IGNORECASE) if script == False else re.compile('\.js$', re.IGNORECASE)
            files = filter(pattern.search, files)
            return files
        except OSError:
            return list()

class Resource(resource.Resource, Storm):
    """The Goliat Resource Object inherits from Twisted Resource and Storm
    This Object only exists for convenience
    """ 
    def __init__(self):
        resource.Resource.__init__(self)
    
    def createTable(self):
        """Create the object table at defined schema database"""
        table = self.getTable()
        if table == None:
            raise DatabaseException('{0} does not exist on schema.yaml, revise your schema definition'.format( self.__storm_table__ ))        
        self.execute('create', table['script'])                 
    
    def dropTable(self):
        """Drop the object table"""
        table = self.getTable()
        if table == None:
            raise DatabaseException('{0} does not exist on schema.yaml, revise your schema definition'.format( self.__storm_table__ ))
        self.execute('drop', table['script'])
    
    def getTable(self):
        gen = Generator(False)
        gen.generateDatabase()
        table = None
        for t in gen.getDatabase():
            if t['name'] == self.__storm_table__:
                table = t
                break
        return table
    
    def execute(self, cmd, script):
        db = Database()
        db.connect()
        dCmd = getattr(db, cmd)        
        dCmd(script)
        