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
# $id goliat/environment/__init__.py created on 05/09/2010 15:12:56 by damnwidget $
'''
Created on 05/09/2010 15:12:56

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary:
@version: 0.1
'''

goliat_environment='production'

def set_environment(environment):
    """
    Sets the Goliat environment.
    """

    goliat_environment=environment

def get_environment():
    """
    Gets the actual Goliat environment.
    """

    return goliat_environment

_all__=['goliat_environment', 'set_environment', 'get_environment']
