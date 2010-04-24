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
# $id Goliat/src/goliat/cli/__init__.py created on 03/04/2010 23:01:34 by damnwidget
'''
Created on 03/04/2010 23:01:34

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary: Goliat Command Line Interface
@version: 0.1
'''
from __future__ import print_function
import sys
from goliat.cli.utils.output import *
class Command(object):
    """Abstract class for all Goliat commands
    
    Taken from Gentoo equery.
    Copyright 2003-2004 Gentoo Technologies, Inc.
    """
    def __init__(self):
        pass
    def short_help(self):
        """Return a help formatted to fit a single line, approx 70 characters.
        Must be overridden in the subclass."""
        return " - not implemented yet"
    def long_help(self):
        """Return full, multiline, color-formatted help.
        Must be overridden in the subclass."""
        return "help for syntax and options"
    def perform(self, args):
        """Stub code for performing the command.
        Must be overridden in the subclass"""
        pass
    def parse_args(self, args):
        """Stub code for parsing command line arguments for this command.
        Must be overridden in the subclass."""
        pass

def build_reverse_map(m):
    r={}
    for x in m.keys():
        r[m[x]]=x
    return r

def userquery(prompt):
    """
    Taken from Gentoo _emerge.userquery and adapted to Goliat. 
    """
    responses=["Yes", "No"]
    colours=[
        create_color_func('green'),
        create_color_func('red')
    ]
    colours=(colours*len(responses))[:len(responses)]
    print('\n'+bold(prompt), end=' ')
    try:
        while True:
            response=raw_input("["+"/".join([colours[i](responses[i]) \
                for i in range(len(responses))])+"] ")
            if response:
                for key in responses:
                    # An empty response will match the
                    # first value in responses.
                    if response.upper()==key[:len(response)].upper():
                        return key
            print("Sorry, response '%s' not understood.".format(response),
                  end=' ')
    except (EOFError, KeyboardInterrupt):
        print('Interrupted.')
        sys.exit(1)

def userchoice(prompt, choices, help):
    """
    Choices menu for user input.
    
    The user get a menu with help content for choices index followed
    by a numeric index value.
    The user just choose a numeric index for his choice and this
    choice is returned.
    """
    colours=[
        create_color_func('green')
    ]
    print('\n'+bold(prompt), end='\n')
    try:
        while True:
            for choice in choices:
                print(colours[0](help[choices.index(choice)].ljust(30))+\
                    " ["+bold(str(choices.index(choice)))+"]")
            response=raw_input("["+"/".join([str(choices.index(choices[i])) \
                for i in range(len(choices))])+"] ")
            if response:
                for key in choices:
                    # An empty response will match the
                    # first value in responses.
                    if response==str(choices.index(key))[:len(response)]:
                        return key
            print("Sorry, response '{0}' not understood.".format(response),
                  end='\n')
            print('\n'+bold(prompt), end='\n')
    except (EOFError, KeyboardInterrupt):
        print('Interrupted.')
        sys.exit(1)

def userinput(prompt):
    """
    User input
    """
    print('\n'+bold(prompt), end='\n')
    try:
        response=raw_input('$ ')
        if response:
            return response
    except (EOFError, KeyboardInterrupt):
        print('Interrupted.')
        sys.exit(1)
