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
# $id goliat/cli/utils/test/test_linux.py created on 23/06/2011 04:44:34 by damnwidget $
'''
Created on 23/06/2011 04:44:34

@license: GPLv2
@copyright: © 2010 - 2011 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: damnwidget
@contact: oscar.campos@open-phoenix.com
@summary: Linux tests.
@version: 0.2
'''

from twisted.trial import unittest

from goliat.cli.utils import linux 

class LinuxTest(unittest.TestCase):
    def setUp(self):
        self.options = {
            'app_name' : 'Test', 'app_version' : '0.1b',
            'app_config' : {}, 'app_layout' : 'two_columns_fh',
            'app_desc' : 'No desc', 'app_port' : '8080',
            'goliat_ver' : '0.2', 'app_file' : 'test.py',
            'app_log' : 'test.log',
        }
    
    def test_generate_tac_file(self):                
        self.assertIsInstance(linux.tac_file(self.options), unicode)
    
    def test_generate_main_js_file(self):
        self.assertIsInstance(linux.main_js_file(self.options), unicode)
    
    def test_generate_project_file(self): 
        self.assertIsInstance(linux.project_file(self.options), unicode)
    
    def test_generate_init_file(self):
        self.assertIsInstance(
            linux.init_file({'share' : 'no share'}, self.options), unicode)
    
    def test_generate_schema_file(self):
        self.assertIsInstance(linux.schema_file(), unicode)
    
    def test_is_supported_distro_success(self):
        self.assertTrue(linux.is_supported('gentoo'))
    
    def test_is_supported_distro_fail(self):
        self.assertFalse(linux.is_supported('mint'))
    