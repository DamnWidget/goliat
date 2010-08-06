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
# $id goliat/session/user.py created on 11/05/2010 03:57:28 by damnwidget $
'''
Created on 11/05/2010 03:57:28

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary:
@version: 0.1
'''
import datetime
import yaml
from zope.interface import Interface, Attribute, implements
from twisted.python.components import registerAdapter
from storm.properties import Int, Unicode, Bool, DateTime

from goliat.session import GoliatSession
from goliat.utils.borg import Borg
from goliat.database import Database
from goliat.auth.acl import Acl
from goliat.template import TemplateManager
from goliat.utils.config import ConfigManager
from goliat.session.userstore import UserStore


class UserProfileException(Exception):
    pass

class IUserProfile(Interface):
    id=Attribute("The profile id")
    user_id=Attribute("The profile associated user's id")
    __storm_table__=Attribute("The Storm table associated to the profile")

class IUser(Interface):
    userdata=Attribute("An UserData object that contains the stored user data")

    def get_name(self):
        """Return the username."""

    def get_uid(self):
        """Return the userid."""

    def get_session(self):
        """Return the user's session."""

class UserData(object):
        """
        User database table abstraction.
        """

        __storm_table__='goliat_user'
        id=Int(primary=True)
        username=Unicode(allow_none=False)
        password=Unicode(allow_none=False)
        groups=Unicode()
        created_on=DateTime()
        last_login=DateTime()
        is_active=Bool(value_factory=True)
        superuser=Bool(value_factory=False)

        def __init__(self, username='', password=''):
            """
            Initialized the object.
            """
            super(UserData, self).__init__()
            self.username=unicode(username)
            self.password=unicode(password)

        def set_username(self, username):
            """
            Set the username.
            """
            self.username=unicode(username)

        def set_password(self, password):
            """
            Set the password.
            """
            self.password=unicode(password)

        def set_groups(self, groups=[]):
            """
            Set the groups
            """
            self.groups=unicode(','.join(groups))

        def set_creation_date(self):
            """
            Set the creation datetime.
            """
            self.created_on=datetime.datetime.now()

        def set_last_login(self):
            """
            Set the last login datetime.
            """
            self.last_login=datetime.datetime.now()

        def activate(self):
            """
            Activate the user.
            """
            self.is_active=True

        def deactivate(self):
            """
            Deactivate the user.
            """
            self.is_active=False

        def set_superuser(self, value):
            """
            Set the superuser flag.
            """
            self.superuser=value

class UserDataProxy(object):

    def __init__(self, username='', password=''):
        self.data_object=UserData(username, password)
        self.store=UserStore().get_store()

    def load(self, userid):
        """
        Load an user object from database.
        """
        self.data_object=UserStore().get_store().get(UserData, int(userid))
        UserStore().get_store().rollback()
        #self.data_object=self.store.get(UserData, int(userid))
        #self.store.rollback()

    def save(self):
        """
        Save the actual user object to the database.
        """
        UserStore().get_store().commit()
        #self.store.commit()

    def __getattr__(self, name):
        return getattr(self.data_object, name)

class UserProfileProxy(object):

    def __init__(self):
        cfg=ConfigManager().get_config('Goliat')
        self.user_profile_class=cfg['Project'].get(
            'user_profile_class', 'UserProfile')
        import_string='application.model.{0}'.format(self.user_profile_class)
        try:
            _temp_module=__import__(import_string, globals(), locals(),
                [self.user_profile_class])
            if IUserProfile.implementedBy(
                getattr(_temp_module, self.user_profile_class)):
                self.user_profile=\
                    getattr(_temp_module, self.user_profile_class)()
                self._raw_module=getattr(_temp_module,
                    self.user_profile_class)
            else:
                err_msg='{0} does not implement IUserProfile Interface'.format(
                    self.user_profile_class)
                raise UserProfileException(err_msg)
            self.store=UserStore().get_store()
        except ImportError:
            self.user_profile=None
            self.store=None

    def load(self, userid):
        """Loads the user profile."""
        if self.user_profile:
            #find_str='.user_id == {0}'.format(userid)            
            prf=UserStore().get_store().find(
                self._raw_module,
                self._raw_module.user_id==userid).one()
            UserStore().get_store().rollback();
            #self.store.rollback()
            self.user_profile=prf

    def save(self):
        """Saves the user profile."""
        if self.user_profile:
            UserStore().get_store().commit()
            #self.store.commit()

    def __getattr__(self, name):
        if self.user_profile:
            return getattr(self.user_profile, name)
        return None

class User(object):
    """
    An authed user representation object.
    """

    implements(IUser)
    def __init__(self, session):
        self.attributes=dict()
        self.groups=list()
        self.userdata=UserDataProxy()
        self.userprofile=UserProfileProxy()
        self.session=session

    def get_profile(self):
        """Return the user profile if exists."""
        return self.userprofile

    def get_session(self):
        """Return the user's session."""
        return self.session

    def load(self, uid):
        """Loads the uid user from the database."""
        self.userdata.load(uid)
        self.userprofile.load(uid)
        self.groups=self.userdata.groups.split(',')

    def save(self):
        """Store the user into the database."""
        self.userdata.save()

    def set_name(self, name):
        """Set the user's name."""
        self.userdata.set_name(name)

    def set_password(self, password):
        """Set the user's password on database."""
        self.userdata.set_password(password)

    def set_attribute(self, key, value):
        """
        Set an attribute value.
        """
        self.attributes[key]=value

    def set_last_login(self):
        """Set the users last login datetime."""
        self.userdata.set_last_login()

    def add_group(self, group_name):
        """Add a group to the user's groups list."""
        self.usergroup.append(group_name)

    def remove_group(self, group_name):
        """Remove a group from the user's groups list."""
        if group_name in self.groups:
            self.groups.remove(group_name)

    def set_groups(self):
        """Set the user groups and store it on database."""
        self.userdata.set_groups(self.groups)

    def get_groups(self):
        """Return a list of groups that this user belongs to."""
        return self.groups

    def get_name(self):
        """Return the username."""
        return self.userdata.username

    def get_uid(self):
        """Return the userid."""
        return self.userdata.id

    def get_attribute(self, key):
        """
        Get an attribute value.
        """
        return self.attributes.get(key)

    def get_creation_date(self):
        return self.userdata.created_on

    def get_last_login(self):
        return self.userdata.last_login

    def has_access(self, resource, privilege):
        """
        Checks if the user has access to the given resource and privilege.
        """
        for group in self.groups:
            if Acl().check_access(group, resource, privilege):
                return True
        return False

    def is_super_user(self):
        """
        Returns true if the user is the super user.
        """
        return self.userdata.superuser

    def is_active(self):
        """
        Returns true if the user is active.
        """
        return self.userdata.is_active

    def __rpr__(self):
        """
        Representation of a user.
        """
        repr=dict()
        repr['sid']=self.session.uid
        repr['uid']=self.get_uid()
        repr['name']=self.get_name()
        repr['groups']=self.get_groups()
        if self.get_creation_date()!=None:
            repr['creation_date']=self.get_creation_date().isoformat()
        else:
            repr['creation_date']=''
        if self.get_last_login()!=None:
            repr['last_login']=self.get_last_login().isoformat()
        else:
            repr['last_login']=''
        repr['active']=self.is_active()

        return repr


registerAdapter(User, GoliatSession, IUser)

user_sql_data=yaml.load(TemplateManager().get_sys_domain().get_template(
    'tpl/usertable.evoque').evoque())
