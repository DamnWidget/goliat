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
# $id Goliat/src/goliat/cli/database.py created on 14/04/2010 01:30:19 by damnwidget $
'''
Created on 14/04/2010 01:30:19

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary:
@version: 0.1
'''
from goliat.cli import Command, buildReverseMap, userquery
from goliat.cli.utils.output import bold, white, turquoise, purple, red, yellow, green, blue, brown
from goliat.database import Database, Generator
import sys

_version = ('Database', '0.1.0')

class CmdCreate(Command):
    """Create a new Goliat project database"""
    def __init__(self):
        self._default_opts = { 'verbose' : False }
        self._valid_opts = ['-v', '--verbose']        
    
    def parseArgs(self, args):
        opts = self._default_opts
        need_help = False
        
        for i in xrange(len(args)):
            x = args[i]
            
            if x in ['-h', '--help']:
                need_help = True
                break;
            elif x in ['-v', '--verbose']:
                opts['verbose'] = True
            else:
                continue;
        
        if need_help:
            print self.longHelp()
            sys.exit(-1)
        
        return opts
    
    def perform(self, args):
        opts = self.parseArgs(args)
        if userquery('ATENTION: This command will delete any project tables at database server.\nWould you like yo continue?') == 'no':
            print '\nQuitting.'
            sys.exit(1) 
        print '\n'+bold('Creating tables...')
        gen = Generator(opts['verbose'])        
        gen.generateDatabase()
        tables = gen.getDatabase()
        db = Database()
        db.connect()
        
        for table in tables:
            if opts['verbose']:
                print bold('Creating table {0}...'.format( table['name'] ))
            db.create(table['script'])
        
        print bold('Database created successfully.')
    
    def shortHelp(self):
        return green("<local-opts> - create a new Goliat project database (create --help for detailed help)")
    
    def longHelp(self):
        return bold("Crate a new Goliat project database.") + \
            "\n" + \
            bold("Syntax:\n") + \
            " " + green("create <local-opts> <application-name>\n") + \
            " " + yellow("--verbose        ") + green("   - run in verbose mode\n")
  

class CmdSql(Command):
    """Prints Goliat project database a standard output"""   
    def parseArgs(self, args):        
        need_help = False
        
        for i in xrange(len(args)):
            x = args[i]
            
            if x in ['-h', '--help']:
                need_help = True
                break;            
        
        if need_help:
            print self.longHelp()
            sys.exit(-1)
        
        return
    
    def perform(self, args):        
        self.parseArgs(args)          
        gen = Generator(False)
        gen.generateDatabase()
        tables = gen.getDatabase()                   
        
        for table in tables:
            if gen.getSqlType() in ['sqlite', 'postgres']:
                print '-----------------------------------------------------------------------------'
                print '-- {0}'.format( table['name'] )
                print '-----------------------------------------------------------------------------'                
            else:
                print '#-----------------------------------------------------------------------------'
                print '#-- {0}'.format( table['name'] )
                print '#-----------------------------------------------------------------------------'
            print table['script']
                
    
    def shortHelp(self):
        return green("<local-opts> - dump a Goliat project database SQL script to standard output (create --help for detailed help)")
    
    def longHelp(self):
        return bold("Dump a Goliat project database to the standard output.") + \
            "\n" + \
            bold("Syntax:\n") + \
            " " + green("create <local-opts> <application-name>\n")
               

_known_commands = {
    'create'    : CmdCreate(),
    'sql'       : CmdSql()      
}
    
_short_commands = {
    'c' : 'create',
    's' : 'sql',
}


def printUsage():
    """Print full usage information for this tool"""
    short_cmds = buildReverseMap(_short_commands)
        
    print bold('Usage: goliat database command <local opts>\n') + \
    bold('where command(short) is one of\n')
    keys = _known_commands.keys()
    keys.sort()
    for x in keys:
        print ' ' + yellow(x) + bold('(') + turquoise(short_cmds[x]) + bold(') ') + \
        green(_known_commands[x].shortHelp())
        
def printVersion():
    """Print the version of this tool"""
    print bold('Database Tool v{0} - Goliat Database Manager\n'.format( _version[1] )) + \
    bold('Copyright (C) 2010 Open Phoenix IT SCA\n') + \
    bold('Author(s): Oscar Campos Ruiz')
    
def parseArgs(args):
    """Parse tool specific arguments.
        
    Arguments are on the form goliat database <tool-specific> [command] <command-specific>
    This method will only parse the <too-specific> bit.
    """
    command = None
    local_opts = []
    showhelp = False
        
    def expand(x):
        if x in _short_commands.keys():
            return _short_commands[x]
        return x
        
    for i in xrange(len(args)):
        x = args[i]
            
        if x in ['-h', '--help']:
            showhelp = True
        elif x in ["-V"]:
            printVersion()
            sys.exit(0)
        elif expand(x) in _known_commands.keys():
            command = _known_commands[expand(x)]
            local_opts.extend(args[i+1:])
            if showhelp:
                local_opts.append("--help")
            break
        else:
            if x not in ['database']: local_opts.append(x)
        
    if not command and showhelp:
        printUsage()
        sys.exit(0)   
        
    return (command, local_opts)
