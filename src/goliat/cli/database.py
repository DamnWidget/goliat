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
from goliat.database import Database, _type_properties
try:
    from storm.twisted.store import DeferredStore as Store
except ImportError:
    from storm.store import Store
from storm.exceptions import OperationalError
from storm.uri import URI
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

class Generator(object):
    def __init__(self, verbose):
        self._verbose = verbose
        self._tables = []
        self._sqlType = ''
    
    def generateDatabase(self):       
        try:
            db = Database()
        except Exception, e:
            print '\n'+red(e[0])
            print '\nAborting'
            exit(-1)
        if self._verbose: print bold('Fixing null values on schema...')        
        db.fixTables()
        if self._verbose:
            print green('Schema fixed!')
            print bold('Retrieving database configuration...')
        dbconfig = db.getSchema().getProperties()
        uri = URI(dbconfig['uri'])
        if self._verbose:
            if uri.scheme == 'sqlite':
                print bold('Trying to connect to {0} database'.format( uri.database ))
            else:            
                print bold('Trying to connect to {0} server on {1} port {2} database {3} with user {4} and passsword {5}...'.format( 
                    uri.scheme.capitalize(), uri.host, uri.port, uri.database, uri.username, uri.password ) )
        self._sqlType = uri.scheme
            
        for table, columns in db.getSchema().getTables().iteritems():
            self._createTable(table, columns)  
    
    def getDatabase(self):
        return self._tables  
    
    def getSqlType(self):
        return self._sqlType
    
    def getSqlQuotes(self):
        if self._sqlType == 'postgres': return '"'
        if self._sqlType == 'mysql': return "`"
        else: return ""
        
    def _createTable(self, table, columns):
        query = "DROP TABLE "
        if self._sqlType == 'postgres':
            query += "{0}{1}{2} CASCADE;\n\n".format( self.getSqlQuotes(), table, self.getSqlQuotes() )
        if self._sqlType == 'mysql':
            query += "IF EXISTS {0}{1}{2};\n\n".format( self.getSqlQuotes(), table, self.getSqlQuotes() )
        if self._sqlType == 'sqlite':
            query += '{0};\n\n'.format( table )
        query += "CREATE TABLE {0}{1}{2}\n".format( self.getSqlQuotes(), table, self.getSqlQuotes() )
        query +="(\n" 
        for column in columns:
            if column in ['_config', '_indexes', '_behaviors']:
                continue
            query += "    {0}{1}{2} ".format( self.getSqlQuotes(), column, self.getSqlQuotes() )            
            query += self._parseColumn(columns[column])
            query += ',\n'
        
        # MySQL and PostgreSQL PRIMARY KEYS
        if self._sqlType in ['mysql', 'postgres']:
            query += '    PRIMARY KEY ( '
            query += self._getPrimaryKeys(columns)
            query += ' )'
        query += "\n);\n"
        
        tb = { 'name' : table, 'script' : query }
        
        self._tables.append(tb)
            
    def _parseColumn(self, data):
        ret = ''
        # Common SQL stuff
        if data.get('type') != None:
            try:
                _type = _type_properties[self._sqlType][data['type'].lower()]
            except KeyError, e:
                print red('The {0} type is not a valid type, revise your yaml definition.'.format( e[0] ))
                sys.exit(-1)
                
            size = ''
            if data.get('size') != None:
                if self._sqlType != 'sqlite':
                    size = '({0}) '.format( data['size'] )
            if data.get('primaryKey') != None:
                if self._sqlType == 'postgres':
                    if _type in ['SMALLINT', 'INT']:
                        _type = 'serial'
                    if _type in ['BIGINT']:
                        _type = 'bigserial'
            ret += '{0}{1} '.format( _type, size )        
        
        if data.get('default') != None:
            ret += 'DEFAULT '
            if type(data['default']) == bool:                
                ret += 'true ' if data['default'] else 'false '
            else:
                ret += '{0} '.format( data['default'] )
        
        if data.get('required') != None:
            ret += 'NOT NULL ' if data['required'] else ''
        
        if data.get('autoIncrement') != None:
            if self._sqlType == 'mysql':
                ret += 'AUTO_INCREMENT '
            elif self._sqlType == 'sqlite':
                ret += 'PRIMARY KEY'
        
        return ret
    
    def _getPrimaryKeys(self, columns):
        if self._sqlType == 'sqlite':
            return 
        
        columnsList = []        
        for name, property in columns.iteritems():
            if name in ['_config', '_beavior']:
                continue
            if 'primaryKey' in property:
                columnsList.append('{0}{1}{2}'.format( self.getSqlQuotes(), name, self.getSqlQuotes() ))
        
        return ','.join(columnsList)
                

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
