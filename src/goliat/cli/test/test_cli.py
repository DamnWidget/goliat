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
# $id goliat/cli/test/test_cli.py created on 28/06/2011 01:52:21 by damnwidget $

'''
Created on 28/06/2011 01:52:21

@license: GPLv2
@copyright: © 2010 - 2011 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: damnwidget
@contact: oscar.campos@open-phoenix.com
@summary: Cli tests
@version: 0.2
'''

from twisted.trial import unittest

from goliat import cli

class CliTest(unittest.TestCase):
    """
    Unit Tests for Goliat Command Line Tools at goliat.cli
    """
    
    def test_build_reverse_map(self):
        """Unit Test for build_reverse_map"""
        rmap = cli.build_reverse_map({'a' :1, 'b':2, 'c':3})        
        self.assertEqual({1 :'a', 2:'b', 3:'c'}, rmap)
        
    def test_userquery_yes(self):
        """
        Unit Test for userquery when input is 'Yes'
        """
        prompt = "Is this an Unit Test?"
        cli.raw_input = lambda _: 'Yes'
        self.assertEqual('Yes', cli.userquery(prompt))
    
    def test_userquery_no(self):
        """
        Unit Test for userquery when input is 'No'
        """
        prompt = "Is this an Unit Test?"
        cli.raw_input = lambda _: 'No'
        self.assertEqual('No', cli.userquery(prompt))   
    
    def test_userchoice(self):
        """Unit Test for userchoice"""
        prompt = "Get it real"
        cli.raw_input = lambda _: '0'
        c = {'No' : 'Of course not', 'Yes' : 'Of course yes'}
        self.assertEqual('Yes', cli.userchoice(prompt, c.keys(), c.values()))
    
        
