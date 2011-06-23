# -*- coding: utf-8 -*-
##
# Goliat: The Twisted and ExtJS Web Framework
# Copyright (C) 2010 - 2011 Open Phoenix IT
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
# $id goliat/utils/test/apply.py created on 22/06/2011 22:13:01 by damnwidget $
'''
Created on 22/06/2011 22:13:01

@license: GPLv2
@copyright: © 2010 - 2011 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: damnwidget
@contact: oscar.campos@open-phoenix.com
@summary: Apply tests-
@version: 0.2
'''

from twisted.trial import unittest
from goliat.utils import apply

class ApplyTest(unittest.TestCase):
    def setUp(self):
        self.item1 = {'a' : 1}
        self.item2 = {'b' : 2}
        self.item3 = {'a' : 1, 'b' : 2}
        
    def test_apply(self):
        self.assertEqual(apply.Apply(self.item1, self.item2), self.item3)
    
    def test_applyif(self):
        self.assertEqual(apply.ApplyIf(self.item1, self.item2), self.item3)        
