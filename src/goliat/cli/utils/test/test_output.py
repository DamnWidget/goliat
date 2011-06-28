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
# $id goliat/cli/utils/test/test_output.py created on 27/06/2011 23:59:29 by damnwidget $

'''
Created on 27/06/2011 23:59:29

@license: GPLv2
@copyright: © 2010 - 2011 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: damnwidget
@contact: oscar.campos@open-phoenix.com
@summary: Gentoo Output tests.
@version: 0.2
'''

from twisted.trial import unittest

from goliat.cli.utils import output

class OutputTest(unittest.TestCase):
    """
    Unit Tests for Gentoo Output tools at goliat.cli.utils
    """
    
    def test_output_reset(self):
        """Unit Test for resetColor"""
        self.assertIdentical(output.codes['reset'], output.resetColor()) 
    
    def test_style_2_ansi(self):
        """Unit Test for style_to_ansi_code"""        
        self.assertEqual(u'\x1b[34m', output.style_to_ansi_code('PKG_NOMERGE'))
    
    def test_colorize(self):
        """Unit Test for colorize"""
        self.assertEqual(u'\x1b[37;01mWhite Test\x1b[39;49;00m',
                         output.colorize('white', 'White Test'))
    
    def test_create_color_func(self):
        """Unit Test for create_color_func"""
        
        self.assertEqual(u'\x1b[37;01mWhite Test\x1b[39;49;00m',
                         output.create_color_func('white')('White Test'))    
    
