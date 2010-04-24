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
# $id goliat/modules.py created on 02/04/2010 23:33:11 by damnwidget
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
class Module(object):
    """Base class for modules.
    
    Every module will declare his url_path.
    """
    _url_path=None
    _object=None
    _name=None
    _loaded=False

    def __init__(self, name):
        super(Module, self).__init__()
        self._name=name.replace('.py', '')


    def get_url_path(self):
        return self._url_path

    def get_module(self):
        return self._object

    def get_name(self):
        return self._name

    def load(self):
        if self._loaded:
            return

        _module_name="application.{0}".format(self._name)
        _obj_list=[self._name.capitalize()]
        _temp_module=__import__(_module_name, globals(), locals(), _obj_list)
        # We need an instance, not a class
        self._object=getattr(_temp_module, _obj_list[0])()
        self._url_path=self._object.get_register_path()
        self._loaded=True

    def is_loaded(self):
        return self._loaded
