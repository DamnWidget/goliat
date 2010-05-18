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
# $id /home/damnwidget/Aptana Studio Workspace/Goliat/src/goliat/session/usermanager.py created on 12/05/2010 21:08:54 by damnwidget $
'''
Created on 12/05/2010 21:08:54

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: damnwidget
@contact: oscar.campos@open-phoenix.com
@summary:
@version: 0.1
'''
from goliat.utils.borg import Borg
from goliat.session.user import IUser

class UserManager(Borg):
    """
    Manage logged-in users.
    """

    users={}
    def __init__(self):
        super(UserManager, self).__init__()

    def register(self, user):
        """
        Register a new user in the users registry.
        """
        self.users[user.get_uid()]=user

    def unregister(self, user):
        """
        Unregister an user from the users registry.
        """
        if user.get_uid() in self.users:
            del self.users[user.get_uid()]

    def get_user_by_name(self, user_name):
        """
        Get an user from the users registry using name as key.
        """
        for uid, user in self.users.iteritems():
            if user.get_name()==user_name:
                return self.get(uid)

    def get(self, uid, session=None):
        """
        Get an user from the users registry, or create a new one if session is
        a valid session, otherwise return None.
        """
        if uid in self.users:
            return self.users[uid]

        if session!=None and session.is_authed():
            user=IUser(session)
            try:
                user.load(uid)
                self.register(user)
                return user
            except:
                pass

        return None

    def exists(self, uid):
        """
        Returns true if the user identified by uid exists, otherwise returns
        false.
        """
        return uid in self.users

