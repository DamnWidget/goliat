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
# $id goliat/cli/database.py created on 14/04/2010 01:30:19 by damnwidget $
'''
Created on 14/04/2010 01:30:19

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary:
@version: 0.2
'''
import sys

from goliat.cli import Command, build_reverse_map, userquery
from goliat.cli.utils.output import *
from goliat.database import Database, Generator

_version=('Database', '0.2.0')

class CmdCreate(Command):
    """Create a new Goliat project database"""
    def __init__(self):
        self._default_opts={ 'verbose' : False }
        self._valid_opts=['-v', '--verbose']

    def parse_args(self, args):
        opts=self._default_opts
        need_help=False

        for i in xrange(len(args)):
            x=args[i]

            if x in ['-h', '--help']:
                need_help=True
                break;
            elif x in ['-v', '--verbose']:
                opts['verbose']=True
            else:
                continue;

        if need_help:
            print self.long_help()
            sys.exit(-1)

        return opts

    def perform(self, args):
        opts=self.parse_args(args)
        if userquery('ATENTION: This command will delete any project tables at'\
                   ' database server.\nWould you like yo continue?')=='no':
            print '\nQuitting.'
            sys.exit(1)
        print '\n'+bold('Creating tables...')
        gen=Generator(opts['verbose'])
        gen.generate_database()
        tables=gen.get_database()
        db=Database()
        db.connect()

        for table in tables:
            if opts['verbose']:
                print bold('Creating table {0}...'.format(table['name']))
            db.create(table['script'])

        print bold('Database created successfully.')

    def short_help(self):
        return green("<local-opts> ")+"- create a new Goliat project database "\
            "(create --help for detailed help)"

    def long_help(self):
        return "Crate a new Goliat project database.\n" \
            "Syntax:\n" \
            " "+green("create <local-opts> <application-name>\n")+\
            " "+yellow("--verbose        ")+"   - run in verbose mode\n"


class CmdSql(Command):
    """Prints Goliat project database a standard output"""
    def parse_args(self, args):
        need_help=False

        for i in xrange(len(args)):
            x=args[i]

            if x in ['-h', '--help']:
                need_help=True
                break;

        if need_help:
            print self.long_help()
            sys.exit(-1)

        return

    def perform(self, args):
        self.parse_args(args)
        gen=Generator(False)
        gen.generate_database()
        tables=gen.get_database()

        for table in tables:
            if gen.get_sql_type() in ['sqlite', 'postgres']:
                print '---------------------------------------------------' \
                '--------------------------'
                print '-- {0}'.format(table['name'])
                print '----------------------------------------------------' \
                '-------------------------'
            else:
                print '#----------------------------------------------------' \
                '-------------------------'
                print '#-- {0}'.format(table['name'])
                print '#----------------------------------------------------' \
                '-------------------------'
            print table['script']


    def short_help(self):
        return green("<local-opts> ")+"- dump a Goliat project database SQL " \
            "script to standard output (sql --help for detailed help)"

    def long_help(self):
        return "Dump a Goliat project database to standard output.\n" \
            "Syntax:\n" \
            " "+green("sql <local-opts> <application-name>\n")


_known_commands={
    'create'    : CmdCreate(),
    'sql'       : CmdSql()
}

_short_commands={
    'c' : 'create',
    's' : 'sql',
}


def print_usage():
    """Print full usage information for this tool"""
    short_cmds=build_reverse_map(_short_commands)

    print 'Usage: goliat database command <local opts>\n' \
    'where command(short) is one of\n'
    keys=_known_commands.keys()
    keys.sort()
    for x in keys:
        print ' '+x+'('+green(short_cmds[x])+') '+\
        _known_commands[x].short_help()

def print_version():
    """Print the version of this tool"""
    print bold('Database Tool v{0} - Goliat Database Manager\n'\
               .format(_version[1]))+\
    bold('Copyright (C) 2010 Open Phoenix IT SCA\n')+\
    bold('Author(s): Oscar Campos Ruiz')

def parse_args(args):
    """Parse tool specific arguments.
        
    Arguments are on the form goliat database <tool-specific> [command]
    <command-specific>
    This method will only parse the <too-specific> bit.
    """
    command=None
    local_opts=[]
    showhelp=False

    def expand(x):
        if x in _short_commands.keys():
            return _short_commands[x]
        return x

    for i in xrange(len(args)):
        x=args[i]

        if x in ['-h', '--help']:
            showhelp=True
        elif x in ["-V"]:
            print_version()
            sys.exit(0)
        elif expand(x) in _known_commands.keys():
            command=_known_commands[expand(x)]
            local_opts.extend(args[i+1:])
            if showhelp:
                local_opts.append("--help")
            break
        else:
            if x not in ['database']: local_opts.append(x)

    if not command and showhelp:
        print_usage()
        sys.exit(0)

    return (command, local_opts)
