# -*- coding: utf-8 -*-
##
# Goliat: The Twisted and ExtJS Web Framework
# Copyright (C) 2010 - 2011 Open Phoenix IT
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
# $id goliat/xmlrpc/store.py created on 17/05/2010 22:08:51 by damnwidget $
'''
Created on 17/05/2010 22:08:51

@license: GPLv2
@copyright: © 2010 - 2011 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary:
@version: 0.2
'''
from twisted.web.xmlrpc import Proxy

class XMLRPCStore(object):
    """
    An store for XMLRPC query responses.
    """

    def __init__(self, url):
        """
        Initialize the store. 
        """
        self.store=dict()
        self.url=url
        self.proxy=Proxy(self.url)
        self.error=False

    def load(self, method, *args):
        """
        A wrapper around L{Proxy.callRemote} to fill the internal store
        """
        return self.proxy.callRemote(method, *args).addCallbacks(
            self.store_values, self.proccess_error)

    def execute(self, method, *args):
        """
        A wrapper around L{Proxy.callRemote} that doesn't fill the store.
        """
        return self.proxy.callRemote(method, *args)

    def store_values(self, values):
        """
        Store returned values from L{Proxy.callRemote}
        """
        if values==False:
            return

        self.store=values

    def proccess_error(self, error):
        """
        Set the error string and set error flag to true
        """
        self.error=True
        self.error_string=error

    def get_error(self):
        """
        Return the error msg
        """
        return self.error_string

    def get_data(self):
        """
        Return the store data.
        """
        return self.store

    def has_errors(self):
        """
        Return true if the query returned an error, otherwhise return false
        """
        return self.error

    def __getattr__(self, name):
        if self.has_errors():
            return None

        return self.store.get(name)

