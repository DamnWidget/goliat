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
# $id goliat/database/reference.py created on 07/05/2010 13:42:47 by damnwidget $
'''
Created on 07/05/2010 13:42:47

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: damnwidget
@contact: oscar.campos@open-phoenix.com
@summary: Abstraction over Reference and DeferredReference
@version: 0.1
'''
from storm.references import Reference as StormReference
from storm.references import ReferenceSet as StormReferenceSet
from storm.twisted.wrapper import DeferredReference, DeferredReferenceSet

from goliat.utils import config

_cfg=config.ConfigManager().look_at_cur_path()

if _cfg.get_config('project')['Project']['tos']:
    class Reference(DeferredReference):
        pass

    class ReferenceSet(DeferredReferenceSet):
        pass
else:
    class Reference(StormReference):
        pass

    class ReferenceSet(StormReferenceSet):
        pass
