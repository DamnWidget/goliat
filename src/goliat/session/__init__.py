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
# $id goliat/session/__init__.py created on 10/05/2010 21:13:26 by damnwidget $
'''
Created on 10/05/2010 21:13:26

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary:
@version: 0.1
'''
import string
from zope.interface import implements
from twisted.python import log
from twisted.cred import error
from twisted.cred.credentials import UsernamePassword, Anonymous, IAnonymous
from twisted.web.resource import IResource, ErrorPage
from twisted.python.components import proxyForInterface
from twisted.web.server import Session
from twisted.web import util
from twisted.python.filepath import FilePath

from goliat.auth import SessionCookie, ISessionCookie
from goliat.auth.login import Login

class GoliatSession(Session):
    """Goliat users session."""
    authed=False

    def authenticate(self):
        self.authed=True

    def is_authed(self):
        return self.authed

    def set_life_time(self, lifetime):
        """Set the lifetime of this session in seconds."""
        self.sessionTimeout=lifetime

class UnauthorizezResource(object):
    """
    Simple IResource to escape Resource dispatch
    """
    implements(IResource)
    isLeaf=True

    def render(self, request):
        """
        Create a custom or generic Login/Access to the Application.
        """
        file=FilePath('custom/unauthorized.py')
        if file.exists() and file.isfile() or file.islink():
            # Custom form is provided
            from custom.login import CustomLogin
            root=IResource(CustomLogin())
        else:
            from goliat.auth.login import Login
            from goliat.utils.config import ConfigManager
            root=IResource(Login(
                ConfigManager().get_config('Goliat')['Project']))

        return root.render(request)

    def getChildWithDefault(self, path, request):
        """
        Disable resource dispatch
        """
        return self

class SessionManager(object):
    """
    SessionManager
    """
    implements(IResource)
    isLeaf=False

    session_life_time=60
    sessions=set()

    def __init__(self, portal):
        """
        Initialize a session wrapper
        """
        self._portal=portal

    def render(self, request):
        """
        Find the L{IResource} avatar suitable for the given request, if
        possible, and render it.  Otherwise, perhaps render an error page
        requiring authorization or describing an internal server failure.
        """
        return self._authorizedResource(request).render(request)

    def getChildWithDefault(self, path, request):
        request.postpath.insert(0, request.prepath.pop())
        return self._authorizedResource(request)

    def check_credentials(self, request):
        if request.args.get('username')==None \
        or request.args.get('password')==None:
            return False

        return True

    def get_credentials(self, request):
        username=request.args.get('username', [''])[0]
        password=request.args.get('password', [''])[0]
        return UsernamePassword(username, password)

    def _authorizedResource(self, request):
        """
        Get the L{IResource} which the given request is authorized to receive.
        If the proper authorization 
        """
        sess=request.getSession()
        if sess.uid not in self.sessions:
            # New Session
            self.sessions.add(sess.uid)
            sess.notifyOnExpire(lambda: self._expired(sess))

        # Session is authenticated already
        if sess.is_authed():
            return util.DeferredResource(
                self._login(SessionCookie(request), sess))

        # Perform an Anonymous login
        if not self.check_credentials(request):
            return util.DeferredResource(
                self._login(Anonymous(), sess))

        # Try to authenticate the session
        return util.DeferredResource(
            self._login(self.get_credentials(request), sess))

    def _expired(self, session):
        print "Session {0} has expired.".format(session.uid)
        from goliat.session.usermanager import UserManager
        from goliat.session.user import IUser
        user=IUser(session)
        UserManager().unregister(user)
        self.sessions.remove(session.uid)

    def _login(self, credentials, session):
        """
        Get the L{IResource} avatar for the given credentials.
        """
        d=self._portal.login(credentials, None, IResource)
        d.addCallbacks(self._login_success, self._login_fail,
            (credentials, session))
        return d

    def _logout(self, request):
        session=request.getSession()
        if session.authed:
            session.expire()

    def _login_success(self, (interface, avatar, avatarId, logout),
            credentials, session):
        """
        Handle login success by wrapping the resulting L{IResource} avatar
        so that the C{logout} callback will be invoked when rendering is
        complete.
        """
        if IAnonymous.providedBy(credentials):
            pass
        else:
            if not session.is_authed():
                session.authenticate()

            if type(avatarId)==int:
                from goliat.session.usermanager import UserManager
                if not UserManager().exists(avatarId):
                    user=UserManager().get(avatarId, session)
                    user.set_last_login()
                    user.save()

        return ResourceWrapper(avatar)

    def _login_fail(self, result):
        """
        Handle login failure by presenting either another challenge (for
        expected authentication/authorization-related failures) or a server
        error page (for anything else).
        """
        if result.check(error.Unauthorized, error.LoginFailed):
            return UnauthorizezResource()
        else:
            log.err(
                result,
                "SessionManager.getChildWithDefault encountered unexpected "
                "error")
            return ErrorPage(500, None, None)

class ResourceWrapper(proxyForInterface(IResource, 'resource')):
    """
    Wrap an L{IResource}.    
    """
    def getChildWithDefault(self, name, request):
        """
        Pass through the lookup to the wrapped resource, wrapping
        the result in L{ResourceWrapper} to ensure session updates will be
        performed.
        """
        return ResourceWrapper(self.resource.getChildWithDefault(name, request))

    def render(self, request):
        """
        Hook into response generation.
        """
        return super(ResourceWrapper, self).render(request)
