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
# $id goliat/auth/acl.py created on 11/05/2010 14:13:47 by damnwidget $
'''
Created on 11/05/2010 14:13:47

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary: Access Control Lists (ACL) for Goliat
@version: 0.1
'''
import yaml

from goliat.utils.borg import Borg


class GoliatAclError(Exception):
    pass

class GoliatResource(object):
    """A resource is an object that can be accessed by a Role."""


    def __init__(self, name=""):
        """
        Initializes a Goliat Resource.
        """
        self.name=name
        self._privileges={}

    def set_privilege(self, privilege, allow=True):
        """
        Set a Goliat Resource privilege.
        """
        self._privileges[privilege]=allow

    def has_access(self, privilege):
        """
        Check if role has access to the resource.
        """
        if privilege in self._privileges:
            return self._privileges[privilege]
        return False

    def __str__(self):
        """
        String representation of a Goliat Resource.
        """
        rpr=self.name+': '
        for p, a in self._privileges.iteritems():
            rpr+='{0}:{1} '.format(p, a)
        return rpr

class Role(object):
    """
    A role is a representation of an user role.
    """


    def __init__(self, name=""):
        """
        An Acl role has access to resources with specific privileges.
        """
        self.name=name
        self._parents={}
        self._resources={}

    def set_parent(self, parent):
        """
        Sets a parent role for this role.
        """
        self._parents[parent.name]=parent

    def set_resource(self, resource):
        """
        Sets a resource for this role.
        """
        self._resources[resource.name]=resource

    def has_access(self, resource, privilege):
        """
        Checks if the role has access to the given resource and privilege.
        """
        if resource in self._resources:
            if self._resources[resource].has_access(privilege):
                return True

        for parent in self._parents.values():
            if parent.has_access(resource, privilege):
                return True

        return False

    def __str__(self):
        """
        String representation of Role.
        """
        rpr=self.name+":\n"
        rpr+="parents:\n"
        for parent in self._parents.keys():
            rpr+="\t{0}\n".format(parent)
        rpr+="resources:\n"
        for resource in self._resources.values():
            rpr+="\t{0}\n".format(resource.__str__())
        return rpr

class Acl(Borg):
    """
    Manages roles and resources.
    """


    _acl={}
    _initialized=False
    def __init__(self):
        super(Acl, self).__init__()

    def set_role(self, role):
        """
        Set a role.
        """
        self._acl[role.name]=role

    def check_access(self, role, resource, privilege):
        """
        Check the access privileges to the resource for the given role.
        """
        if not role in self._acl:
            raise GoliatAclError('Role does not exists')
        return self._acl[role].has_access(resource, privilege)

    def build(self, file):
        """
        Build an Acl from a YAML configuration file.
        """
        roles={}
        permissions={}
        config=yaml.load(file)

        # Find roles, resources and permissions to create
        for role, cfg in config['roles'].iteritems():
            roles[role]=[]
            permissions[role]=[]
            if cfg.get('inherit')!=None:
                for parent in cfg.get('inherit'):
                    roles[role].append(parent)

            for resource, perms in cfg.iteritems():
                if resource!='inherit':
                    res=GoliatResource()
                    res.name=resource
                    for value in perms:
                        res.set_privilege(value)

                    permissions[role].append(res)

        for role, parents in roles.iteritems():
            self.set_role(self._create_role(role, roles))

        for role_name, resource in permissions.iteritems():
            role=self._acl[role_name]
            for res in resource:
                role.set_resource(res)

        self._initialized=True

    def is_initialized(self):
        """
        Return true if the Acl contains data, false otherwise.
        """
        return self._initialized

    def _create_role(self, role_name, roles):
        """
        Recursively create parent roles and then create child role.
        """
        if role_name in self._acl:
            role=self._acl[role_name]
        else:
            role=Role()
            role.name=role_name

        for parent_name in roles[role_name]:
            if parent_name in self._acl:
                parent=self._acl[parent_name]
            else:
                parent=self._create_role(parent_name, roles)
                self.set_role(parent)
            role.set_parent(parent)

        return role

    def __str__(self):
        """
        String representation of Acl.
        """
        rpr=''
        for role in self._acl.values():
            rpr+='--------------\n'
            rpr+=role.__str__()
        return rpr
