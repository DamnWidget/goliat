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
# $id src/goliat/auth/realm.py created on 12/05/2010 00:14:48 by damnwidget $
'''
Created on 12/05/2010 00:14:48

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary: Goliat default Realm
@version: 0.1
'''
from zope.interface import implements

from twisted.cred.portal import IRealm
from twisted.web.resource import IResource
from twisted.cred import checkers

class GoliatRealm(object):
    """
    Goliat default portal Realm.
    """

    implements(IRealm)
    def __init__(self, root):
        """
        Initializes the Realm.
        """
        self.root=root

    def requestAvatar(self, avatarId, mind, *interfaces):
        if IResource in interfaces:
            avatar=self.root
            return (IResource, avatar, avatarId, lambda: None)
        raise NotImplementedError(
            'Only IResource interface is supported by this realm.')

