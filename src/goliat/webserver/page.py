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
# $id Goliat/src/goliat/webserver/page.py created on 02/04/2010 17:05:12 by damnwidget
'''
Created on 02/04/2010 17:05:12

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary: The Page object is the main application entry point at Goliat Application Webpages.
@version: 0.1
'''
from twisted.web import resource
from goliat._version import version
from goliat.utils.apply import Apply
from goliat.http.headers import Headers
from goliat.modulemgr import ModuleManager
from goliat.webserver.resources import ResourcesLoader
import os

class Page(resource.Resource):
    """The Goliat Page Object.
    
    @var options: The Goliat options for the Page content.   
    """
    _options = {
        'docType'       : 'xhtml-transitional',
        'meta'          : [],
        'styles'        : [],
        'scripts'       : [],
        'title'         : 'Open Phoenix IT, Goliat Webservice v{0} '.format( version.short() ),
        'description'   : 'Goliat {0} is a Webframework over Twsited, Orbited and Storm using ExtJS and OpenPhoenixJS as GUI enhancement. Goliat has been developed by Open Phoenix IT SCA.'.format( version.short() ),
        'language'      : os.environ['LANG'].split('_')[0],
        'rl'            :  {
            'debug'             : False,
            'useOrbited'        : False,        
            'resPath'           : {},
            'extjsTheme'        : 'xtheme-gray',
            'goliatTheme'       : 'goliat-gray'
        }
    }
    
    _header = Headers()
    _loader = None
    _mgr = ModuleManager()
    
    def __init__(self, options=dict()):
        resource.Resource.__init__(self)
        self._options = Apply(self._options, options)
        # Set page language
        self._header.setLanguage(self._options['language'])
        # Set page description
        self._header.setDescription(self._options['description'])
        # Set the ResourcesLoader
        self._loader = ResourcesLoader(self, self._options['rl'])    
        self._loader.Setup(self._mgr)    
    
    def getChild(self, path, request):
        if path == '' or path == None or path == 'index' or path == 'app':
            return self
        
        return resource.Resource.getChild(self, path, request)
    
    def renderGet(self, request):
        """Renders the index page"""
        _page = []        
        a = _page.append
        
        # Create the page headers
        a('%s\n' % self._header.getDocType(self._options['docType']))        
        a('%s\n' % self._header.getHtmlElement())        
        a('    <head>\n')
        a('        {0}\n'.format( self._header.getContentType() ))
        a('        {0}\n'.format( self._header.getGeneratorContent() ))
        a('        {0}\n'.format( self._header.getDescriptionContent() ))
        a('        {0}\n'.format( self._header.getLanguageContent() ))
        a('        {0}\n'.format( self._header.getGoliatContent() ))
        
        media = self._options['resPath']['media'] if 'resPath' in self._options and 'media' in self._options['resPath'] else 'media'
        a('        {0}\n'.format( self._header.getFaviconContent(media) ))
        
        # Iterate over the user defined meta keys and add it to the header's page
        for meta in self._options['meta']:
            a('        {0}\n'.format( meta ))
        
        # Iterate over the user defined styles and add it to the header's page
        for style in self._options['styles']:
            a('        {0}\n'.format( style ))
        
        # Iterate over the user defined scripts and add it to the header's page
        for script in self._options['scripts']:
            a('        {0}\n'.format( script ))
        
        a('        <title>{0}</title>\n'.format( self._options['title'] ))
        a('    </head>\n')
        a('</html>')
        
        # Return the rendered page       
        return ''.join(_page)
    
    def addStyle(self, style):
        """Adds a style to the page"""
        self._options['styles'].append(style)
    
    def addScript(self, script):
        """Adds a script to the page"""
        self._options['scripts'].append(script)
        
    def addMeta(self, meta):
        """Adds a meta to the page hedaer"""
        self._options['meta'].append(meta)
    
    def getModuleManager(self):
        """Returns the page module manager"""
        return self._mgr
