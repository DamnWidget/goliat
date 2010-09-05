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
# $id goliat/branching/__init__.py created on 5/09/2010 12:42:31 by damnwidget $
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

import yaml
from goliat.utils import borg

class Branch(object):
    """
    An object that represents a Version of deployable software.
    """

    def __init__(self, name):
        self._name=name
        self._conditions=[]

    def get_name(self):
        return self._name

    def set_condition(self, cond):
        """
        Sets a condition for the branch.
        """
        self._conditions.append(cond)

    def check_conditions(self, params=None):
        """
        Check Branch conditions.
        """
        for cond in self._conditions:
            if not params:
                if eval(cond):
                    return True
            else:
                if eval(cond%params):
                    return True

        return False


class BranchManager(borg.Borg):
    """
    Manages Branches.
    """

    _branches={}
    def __init__(self):
        super(BranchManager, self).__init__()

    def build(self, file):
        """
        Build a Branch version system from a YAML configuration file.
        """
        config=yaml.load(file)

        # Find branches and condiions to create
        for branch, cfg in config['branches'].iteritems():
            self._branches[branch]=None
            for tag, conds in cfg.iteritems():
                n_branch=Branch(tag)
                for cond in conds:
                    n_branch.set_condition(cond)

                self._branches[branch]=n_branch

    def get_branch(self, name):
        """
        Returns a branch given by name
        """
        if name in self._branches:
            return self._branches[name]
        return None


__all__=["Branch", "BranchManager"]
