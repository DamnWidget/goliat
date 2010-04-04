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
# $id Goliat/src/goliat/http/headers.py created on 02/04/2010 17:16:05 by damnwidget
'''
Created on 02/04/2010 17:16:05

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary: Dummy class needed to maintain other code places clean
@version: 0.1
'''
from goliat._version import version
import platform

class Headers(object):
    """
    An object that build the Application page header and returns it
    as a well formated XHTML/HTML string.    
    """
    _docTypes = {
        'html'      : {
            'strict'        : '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">',
            'transitional'  : '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">',
            'frameset'      : '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd">'
        },
        'xhtml'     : {
            'strict'        : '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">',
            'transitional'  : '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">',
            'frameset'      : '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">'
        }
    }
    
    _htmlElement = '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">'    
    _contentType = '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
    _description = 'Non Description'
    _language = 'en'
    _favicon = 'favicon.ico'        
    
    def getDocType(self, doctype):
        """Translate a L{Goliat.webserver.Page} docType options to a
        valid DOCTYPE Header string.
        
        @return: A valid DOCTYPE Header string        
        """
        type = doctype.split('-')[0]
        dtd = doctype.split('-')[1]        
        if type in self._docTypes:
            if dtd in self._docTypes[type]:
                return self._docTypes[type][dtd]
        
        return ''
    
    def setDocType(self, doctype, val):
        type = doctype.split('-')[0]
        dtd = doctype.split('-')[1]  
        self._docTypes[type] = { dtd : val }
    
    def getHtmlElement(self):
        return self._htmlElement
    
    def setHtmlElement(self, val):
        self._htmlElement = val
    
    def getContentType(self):
        return self._contentType

    def setContentType(self, val):
        self._contentType = val
    
    def getDescription(self):
        return self._description
    
    def setDescription(self, val):
        self._description = val
    
    def getLanguage(self):
        return self._language
    
    def setLanguage(self, val):
        self._language = val
    
    def getFavicon(self):
        return self._favicon
    
    def setFavicon(self, val):
        self._favicon = val
    
    def getLanguageContent(self):
        return '<meta name="language" content="{0}" />'.format( self._language )
    
    def getDescriptionContent(self):
        return '<meta name="description" content="{0}" />'.format( self._description )
    
    def getGeneratorContent(self):
        return '<meta name="generator" content="Goliat Web Application Framework version {0}" />'.format( version.short() )
    
    def getGoliatContent(self):
        return '<meta name="goliat-content" content="Platform: {0};Version: {1};Arch: {2}" />'.format( platform.system(), platform.release(), platform.machine() )    
    
    def getFaviconContent(self, media='/media'):
        return '<link rel="shortcut icon" href="{0}/{1}" />'.format( media, self._favicon )    
     
                