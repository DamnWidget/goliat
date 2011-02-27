# -*- coding: utf-8 -*-
##
# Goliat: The Twisted and ExtJS Web Framework
# Copyright (C) 2010 - 2011  Open Phoenix IT
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
@version: 0.2
'''
from goliat._version import version
import platform

class Headers(object):
    """
    An object that build the Application page header and returns it
    as a well formated XHTML/HTML string.    
    """
    _doc_types={
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

    _html_element='<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">'
    _content_type='<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
    _description='Non Description'
    _language='en'
    _favicon='favicon.ico'

    def get_doc_type(self, doctype):
        """Translate a L{Goliat.webserver.Page} docType options to a
        valid DOCTYPE Header string.
        
        @return: A valid DOCTYPE Header string        
        """
        type=doctype.split('-')[0]
        dtd=doctype.split('-')[1]
        if type in self._doc_types:
            if dtd in self._doc_types[type]:
                return self._doc_types[type][dtd]

        return ''

    def set_doc_type(self, doctype, val):
        type=doctype.split('-')[0]
        dtd=doctype.split('-')[1]
        self._doc_types[type]={ dtd : val }

    def get_html_element(self):
        return self._html_element

    def set_html_element(self, val):
        self._html_element=val

    def get_content_type(self):
        return self._content_type

    def set_content_type(self, val):
        self._content_type=val

    def get_description(self):
        return self._description

    def set_description(self, val):
        self._description=val

    def get_language(self):
        return self._language

    def set_language(self, val):
        self._language=val

    def get_favicon(self):
        return self._favicon

    def set_favicon(self, val):
        self._favicon=val

    def get_language_content(self):
        return '<meta name="language" content="{0}" />'.format(self._language)

    def get_description_content(self):
        return '<meta name="description" content="{0}" />'.format(self._description)

    def get_generator_content(self):
        return '<meta name="generator" content="Goliat Web Application Framework version {0}" />'.format(version.short())

    def get_goliat_content(self):
        return '<meta name="goliat-content" content="Platform: {0};Version: {1};Arch: {2}" />'.format(platform.system(), platform.release(), platform.machine())

    def get_favicon_content(self, media='/media'):
        return '<link rel="shortcut icon" href="{0}/{1}" />'.format(media, self._favicon)

