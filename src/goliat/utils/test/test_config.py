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
# $id goliat/utils/test/config.py created on 22/06/2011 22:24:40 by damnwidget $

'''
Created on 22/06/2011 22:24:40

@license: GPLv2
@copyright: © 2010 - 2011 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: damnwidget
@contact: oscar.campos@open-phoenix.com
@summary: Config tests.
@version: 0.2
'''

import os
from ConfigParser import RawConfigParser, SafeConfigParser, \
    MissingSectionHeaderError
from twisted.trial import unittest

from goliat.utils import config

class ConfigTest(unittest.TestCase):
    def setUp(self):
        cfg_data = "[Project]\n" + \
                   "meta_description = ConfigTest is a Unit Test for Goliat\n" + \
                   "app_name = ConfigTest\n" + \
                   "language = en\n" + \
                   "app_desc = None\n" + \
                   "tos = True\n" + \
                   "allow_anonymous = True\n" + \
                   "doctype = xhtml-transitional\n" + \
                   "meta_keys = UnitTest\n" + \
                   "ext_theme = xtheme-gray\n" + \
                   "version = 0.1b\n" + \
                   "orbited = True\n" + \
                   "app_port = 8080\n" + \
                   "goliat_theme = crystal\n" + \
                   "debug = False\n" + \
                   "app_layout = two_columns_fh\n" + \
                   "admin=shadow\n" + \
                   "password=shadow\n" + \
                   "admin_port=5555\n" + \
                   "respath={ 'doc' : 'web/doc' }\n" + \
                   "\n" + \
                   "[Goliat]\n" + \
                   "version = 0.2.0" 

        cfg_file = open('test.cfg', 'w')
        cfg_file.writelines(cfg_data)
        cfg_file.close()
        
        self.cfg = config.ConfigManager()
    
    def setCommonData(self, cfg_data):
        cfg_file = open('test.cfg', 'w')
        cfg_file.writelines(cfg_data)
        cfg_file.close()        
        
    def test_load_config_file(self):
        self.assertTrue(self.cfg.load_config('Goliat', 'test.cfg', True))
        self.assertFalse(self.cfg.load_config('Tailog', 'notexists.cfg', True))
    
    def test_reload(self):        
        self.cfg.load_config('Goliat', 'test.cfg', True)
        item1 = self.cfg.get_config('Goliat')        
        self.cfg.reload('Goliat', True)
        
        self.assertEqual(item1, self.cfg.get_config('Goliat'))
        
    def test_get_config_success(self):
        self.cfg.load_config('Goliat', 'test.cfg', True)                 
        self.assertIsInstance(self.cfg.get_config('Goliat'), dict)
    
    def test_get_config_fail(self):                        
        self.assertNotIsInstance(self.cfg.get_config('Goliat'), dict)
        self.assertIdentical(None, self.cfg.get_config('Goliat'))
    
    def test_process_raw_config_file_fail(self):
        cfg_data = "None"
        self.setCommonData(cfg_data)
        
        config = {}        
        self.assertRaises(
            MissingSectionHeaderError, self.cfg._process_raw_config_file,
            'Goliat', RawConfigParser(), config)
        
    def test_process_raw_config_file_no_goliat(self):
        cfg_data = "[Project]\nfoo=bar\n"
        self.setCommonData(cfg_data)
        
        conf = {}
        self.assertRaises(config.ConfigManagerException,
                          self.cfg._process_raw_config_file,
                          'Goliat', RawConfigParser(), conf)
    def test_process_config_file_fail(self):
        cfg_data = "None"
        self.setCommonData(cfg_data)
        
        config = {}        
        self.assertRaises(
            MissingSectionHeaderError, self.cfg._process_raw_config_file,
            'Goliat', SafeConfigParser(), config)
        
    def test_process_config_file_no_goliat(self):
        cfg_data = "[Project]\nfoo=bar\n"
        self.setCommonData(cfg_data)        
        
        conf = {}
        self.assertRaises(config.ConfigManagerException,
                          self.cfg._process_config_file,
                          'Goliat', SafeConfigParser(), conf)
        
    def test_look_at_cur_path(self):
        self.assertIsInstance(self.cfg.look_at_cur_path(), config.ConfigManager)
    
    def test_look_at_cur_path_fail(self):
        os.unlink('test.cfg')
        self.assertIdentical(None, self.cfg.look_at_cur_path())
    
    def test_write_config(self):        
        self.assertTrue(self.cfg.load_config('Goliat', 'test.cfg', True))
        origconf = self.cfg.get_config('Goliat')        
        origconf['Project']['debug'] = True
        self.cfg.write_config(origconf)
        self.cfg.reload('Goliat', True)         
        self.assertTrue(self.cfg.get_config('Goliat')['Project']['debug'])
        
        