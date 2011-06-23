# -*- test-case-name: goliat.utils.test.apply -*-
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
# $id Goliat/src/goliat/utils/apply.py created on 02/04/2010 16:16:12 by damnwidget
'''
Created on 02/04/2010 16:16:12

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary: Apply the content of a dict into another dict
@version: 0.1
'''

def Apply(dict1, dict2):
    for k,v in dict2.iteritems():
        dict1[k] = v
    
    return dict1

def ApplyIf(dict1, dict2):
    for k,v in dict2.iteritems():
        if k not in dict1:
            dict1[k] = v

    return dict1