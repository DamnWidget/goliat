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
# $id Goliat/src/goliat/cli/project.py created on 03/04/2010 23:03:15 by damnwidget
'''
Created on 03/04/2010 23:03:15

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: damnwidget
@contact: oscar.campos@open-phoenix.com
@summary: Command Line Interface Project Manager
@version: 0.1
'''
import goliat.cli.utils.linux as linux

_version = ('Project', '0.1.0')

class Project(object):
    """Goliat CLI Project Class.
    """
    _templates = {
        'tacFile'       : None,
        'mainJsFile'    : None,
        'serviceFile'   : None,
        'projectFile'   : None
    }
    
    _installPaths = dict()
    
    def __init__(self, options=dict()):
        """Constructor"""
        self._options = options                
        self._buildInstallPaths()        
    
    def _buildTemplateFiles(self):
        """Setup the template for the project files"""
        
        # Template for twisted tac file
        self._templates['tacFile'] = linux.tacFile(self._installPaths, self._options)
        
        # Template for main.js file 
        self._templates['mainJsFile'] = linux.mainJsFile(self._installPaths, self._options)
        
        self._templates['projectFile'] = linux.projectFile(self._installPaths, self._options) 
        
        self._templates['serviceFile'] = linux.initFile(self._installPaths, self._options)
    
    def _buildInstallPaths(self):
        """Setup the new project application install paths"""       
        self._installPaths['share'] = '/usr/share/goliat/app/{0}'.format( self._options['app_name'].lower() )            
        self._installPaths['service'] = '/etc/init.d'
        self._installPaths['config'] = '/etc/{0}.cfg'.format( self._options['app_name'].lower() )
