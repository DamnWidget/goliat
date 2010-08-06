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
# $id goliat/auth/__init__.py created on 10/05/2010 14:07:31 by damnwidget $
'''
Created on 10/05/2010 14:07:31

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary: Goliat Authentication
@version: 0.1
'''
import hashlib
from zope.interface import implements
from twisted.cred import error, credentials
from twisted.cred.credentials import (
    IUsernameHashedPassword, IUsernamePassword, ICredentials)
from twisted.python import components
from twisted.cred.checkers import ICredentialsChecker
from twisted.web.resource import IResource
from twisted.internet import defer

from goliat.database import Database
from goliat.session.userstore import UserStore

class ISessionCookie(ICredentials):
    def check_session(self):
        """
        Validate cookie credentials.
        """

class SessionCookie:
    implements(ISessionCookie)
    def __init__(self, request):
        self.request=request

    def check_session(self):
        return self.request.getSession().is_authed()

    def get_uid(self):
        return self.request.getSession().uid

class DBCredentialsChecker(object):
    """
    Checks the credentials of incomming connections against a user table in a
    database.
    """
    implements(ICredentialsChecker)

    def __init__(self):
        self.credentialInterfaces=(IUsernamePassword, IUsernameHashedPassword)

    def requestAvatarId(self, credentials):
        """
        Authenticates against the Database.        
        """
        # Check that the credentials instance implements at least one of our
        # interfaces        
        for interface in self.credentialInterfaces:
            if interface.providedBy(credentials):
                break
        else:
            raise error.UnhandledCredentials()
        from goliat.session.user import UserData
        # Ask the database for the username and password        
        result=UserStore().get_store().find(
            UserData, UserData.username==unicode(credentials.username)).one()
        UserStore().get_store().commit()
        # Authenticate the user        
        return self._auth(result, credentials)

    def _auth(self, result, credentials):
        if not result:
            # Username not found in db            
            return defer.fail(
                error.UnauthorizedLogin('Username or Password mismatch'))
        else:
            id=result.id
            password=result.password

        if IUsernameHashedPassword.providedBy(credentials):
            if credentials.checkPassword(password):
                return defer.succeed(id)
            else:
                return defer.fail(
                    error.UnauthorizedLogin('Username or Password mismatch'))
        elif IUsernamePassword.providedBy(credentials):
            m=hashlib.md5()
            m.update(credentials.password)
            #if password==m.hexdigest():
            if password==credentials.password:
                from goliat.session.usermanager import UserManager
                if not UserManager().exists(id):
                    return defer.succeed(id)
                else:
                    return defer.fail(
                        error.LoginFailed('Already Logged'))
            else:
                return defer.fail(
                    error.UnauthorizedLogin('Username or Password mismatch'))
        else:
            # Wooops!            
            return defer.fail(
                error.UnhandledCredentials('Revise the protocol configuration'))

class SessionCookieCredentialsChecker(object):
    """
    Checks the credentials of incomming connections against authenticated
    sessions.
    """
    implements(ICredentialsChecker)

    def __init__(self):
        self.credentialInterfaces=(ISessionCookie,)

    def requestAvatarId(self, credentials):
        """
        Authenticate against authed session.
        """
        for interface in self.credentialInterfaces:
            if interface.providedBy(credentials):
                break
        else:
            raise error.UnhandledCredentials()

        if credentials.check_session():
            return defer.succeed(credentials.get_uid())
        else:
            return defer.fail(
                error.UnauthorizedLogin('Cookie don\'t own an authed session'))
