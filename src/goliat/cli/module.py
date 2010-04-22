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
# $id Goliat/src/goliat/cli/module.py created on 19/04/2010 15:05:00 by damnwidget $
'''
Created on 19/04/2010 15:05:00

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary:
@version: 0.1
'''
from goliat.cli import Command, buildReverseMap
from goliat.cli.utils.output import *
from goliat.model import Generator
from goliat.database.schema import Schema
from goliat.template import TemplateManager
from datetime import datetime
import sys

_version = ('Model', '0.1.0')

class CmdGenerateModule(Command):
    """Create a new Goliat model"""
    def __init__(self):
        self._default_opts = { 'verbose' : False, 'dump' : False }
        self._valid_opts = ['-v', '--verbose', '-d', '--dump', '-l', '--list', '-m', '--model']
    
    def parseArgs(self, args):
        opts = self._default_opts
        need_help = False
        module_name = ''        
        
        for i in xrange(len(args)):
            x = args[i]
            
            if x in ['-h', '--help']:
                need_help = True
                break;
            elif x in ['-v', '--verbose']:
                opts['verbose'] = True
            elif x in ['-d', '--dump']:
                opts['dump'] = True
            elif x in ['-m', '--model']:
                opts['model'] = args[i+1]
            elif x in ['-l', '--list']:
                modelList()
                sys.exit(1)
            elif x.startswith('-') and x not in self._valid_opts:
                continue; 
            else:
                if x not in opts.values():
                    module_name = x
        
        if need_help:
            print self.longHelp()
            sys.exit(-1)
        
        return (module_name, opts)
    
    def perform(self, args):
        module_name, opts = self.parseArgs(args)
        _schema = Schema('config/schema.yaml')
        _schema.fixTables()
        _module_model_import = ''
        _module_database = ''
        _module_model_init = ''
        if opts.get('model') != None:            
            if not checkModel(opts['model']):
                print red('\n{0} model does not exist at the project schema.\nUse module -l or module --list to show a list of available models.'.format( opts['model'] if len(opts['model']) else 'Noname' ))
                sys.exit(0)        
            gen = Generator(opts['verbose']) 
            tmodel = gen.create_m(opts['model'], _schema.findTable(opts['model']))
            _module_model_import='from application.model.{0} import {1}'.format( gen._generateModelName(opts['model']), gen._generateModelName(opts['model']) )
            _module_database='_db = Database().getDatabase()'
            _module_model_init='_store = Store(_db)'
            
        print '\n'+bold('Generating {0} module...'.format( module_name ))
        mgr = TemplateManager()
        t = mgr.getSysDomain().get_template('tpl/module.evoque')
        module =  t.evoque(
            module_file="application/{0}.py".format(module_name),
            module_creation_date=datetime.now(),
            module_name=module_name,
            module_model_import=_module_model_import,
            module_database=_module_database,
            module_model_init=_module_model_init
        )               
        if opts['dump']:            
            if opts.get('model') != None:
                print '\napplication/model/{0}.py'.format(tmodel['work'][0])
                print tmodel['work'][1]
            print '\napplication/{0}.py'.format(module_name)         
            print  module      
        else :
            if opts.get('model') != None:
                gen.writeModel(tmodel['work'][0], tmodel['work'][1])
            fp = file('application/{0}.py'.format(module_name), 'w')
            fp.write(module.encode('utf8'))
            fp.close()            
        
        print bold('Module created successfully.')
    
    def shortHelp(self):
        return green("<local-opts> - generate a new Goliat module (generate --help for detailed help)")
    
    def longHelp(self):
        return bold("Crate a new Goliat module.\n") + \
            "\n" + \
            bold("Syntax:\n") + \
            " " + green("generate-model <local-opts> <module-name>\n") + \
            " " + yellow("-m, --model      ") + green("   - model based on\n") + \
            " " + yellow("-d, --dump       ") + green("   - dump to standard output\n") + \
            " " + yellow("-l, --list       ") + green("   - show a list of available model at current schema\n") + \
            " " + yellow("--verbose        ") + green("   - run in verbose mode\n")
               

_known_commands = {
    'generate'    : CmdGenerateModule()          
}
    
_short_commands = {
    'g' : 'generate'    
}

def modelList():
    """Return a list of available models at current schema"""
    for table in _schema.getTablesList():
        print brown(table)    

def checkModel(model_name):
    """Checks if a model given by model name exists at the current schema"""
    if not len(model_name):
        return False
    
    if not model_name in modelList():
        return False
    
    return True


def printUsage():
    """Print full usage information for this tool"""
    short_cmds = buildReverseMap(_short_commands)
        
    print bold('Usage: goliat module command <local opts>\n') + \
    bold('where command(short) is one of\n')
    keys = _known_commands.keys()
    keys.sort()
    for x in keys:
        print ' ' + yellow(x) + bold('(') + turquoise(short_cmds[x]) + bold(') ') + \
        green(_known_commands[x].shortHelp())
        
def printVersion():
    """Print the version of this tool"""
    print bold('Module Tool v{0} - Goliat Module Manager\n'.format( _version[1] )) + \
    bold('Copyright (C) 2010 Open Phoenix IT SCA\n') + \
    bold('Author(s): Oscar Campos Ruiz')
    
def parseArgs(args):
    """Parse tool specific arguments.
        
    Arguments are on the form goliat model <tool-specific> [command] <command-specific>
    This method will only parse the <tool-specific> bit.
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
            if x not in ['module']: local_opts.append(x)    
    
    if not command and showhelp:
        printUsage()
        sys.exit(0)   
        
    return (command, local_opts)
