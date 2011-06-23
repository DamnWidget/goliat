# -*- test-case-name: goliat.utils.test.borg -*-
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
# $id Goliat/src/goliat/utils/borg.py created on 05/04/2010 02:07:10 by damnwidget $
'''
Created on 05/04/2010 02:07:10

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary: Goliat implementation of Alex Martelli's Borg 'no-pattern'
@version: 0.1
'''
class Borg(object):
    """The Goliat Borg Class.
    
    Every object created using the Borg pattern will share their information, as long as
    they refer to the same state information. This is a more elegant type of singleton, but, 
    in other hand, Borg objects doesn't have the same ID, every object have his own ID
    """
    _shared_state = {}
    def __init__(self):
        self.__dict__ = self._shared_state
