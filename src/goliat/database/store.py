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
# $id goliat/database/Store.py created on 06/05/2010 18:40:10 by damnwidget $
'''
Created on 06/05/2010 18:40:10

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary: Wrapper class above Store and DeferredStore to offer an abstraction
over storm Stores using twisted or not.
@version: 0.1
'''
from storm.store import Store as StormStore
from storm.twisted.store import DeferredStore
from goliat.utils import config

_cfg=config.ConfigManager().look_at_cur_path()

if _cfg.get_config('project')['Project']['tos']:
    class Store(DeferredStore):
        """DeferredStore Wrapper Goliat Class."""

        def __init__(self, database):
            DeferredStore.__init__(self, database)
            self.start()
else:
    class Store(StormStore):
        """Store Wrapper Goliat Class."""

        def __init__(self, database):
            StormStore.__init__(self, database)
