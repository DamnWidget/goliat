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
# $id goliat/cli/model.py created on 15/04/2010 03:52:30 by damnwidget $
'''
Created on 15/04/2010 03:52:30

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary:
@version: 0.1
'''
import sys

from goliat.cli import Command, build_reverse_map
from goliat.cli.utils.output import *
from goliat.model import Generator
from goliat.database.schema import Schema

_version=('Model', '0.1.0')


class CmdGenerate(Command):
    """Create a new Goliat model"""
    def __init__(self):
        self._default_opts={ 'verbose' : False, 'dump' : False }
        self._valid_opts=['-v', '--verbose', '-d', '--dump', '-l', '--list']

    def parse_args(self, args):
        opts=self._default_opts
        need_help=False
        model_name=''

        for i in xrange(len(args)):
            x=args[i]

            if x in ['-h', '--help']:
                need_help=True
                break;
            elif x in ['-v', '--verbose']:
                opts['verbose']=True
            elif x in ['-d', '--dump']:
                opts['dump']=True
            elif x in ['-l', '--list']:
                model_list()
                sys.exit(1)
            elif x.startswith('-') and x not in self._valid_opts:
                continue;
            else:
                if x not in opts.values():
                    model_name=x

        if need_help:
            print self.long_help()
            sys.exit(-1)

        return (model_name, opts)

    def perform(self, args):
        model_name, opts=self.parse_args(args)
        try:
            _schema=Schema('config/schema.yaml')
            _schema.fix_tables()
        except TypeError:
            print red('The schema is not defined.')
            sys.exit(-1)
        if not check_model(model_name):
            print red('\n{0} model does not exist at the project schema.\n' \
            'Use model -l or model --list to show a list of available models.'\
            .format(model_name if len(model_name) else 'Noname'))
            sys.exit(0)
        print '\n'+bold('Generating {0} model...'.format(model_name))
        gen=Generator(opts['verbose'])
        templates=gen.create_b(model_name, _schema.find_table(model_name))
        if opts['dump']:
            print '\napplication/model/base/{0}Base.py'.format(
                templates['base'][0])
            print templates['base'][1]
            if templates.get('rel')!=None:
                for rel in templates['rel']:
                    print '\n\napplication/model/relation/{0}.py'.format(
                        rel[0])
                    print rel[1]
        else :
            gen.write_base_model(templates['base'][0], templates['base'][1])
            if templates.get('rel')!=None:
                for rel in templates['rel']:
                    gen.write_relation(rel[0], rel[1])

        print bold('Model created successfully.')

    def short_help(self):
        return green("<local-opts> ")+"- generate a new Goliat model " \
            "(generate-model --help for detailed help)"

    def long_help(self):
        return "Crate a new Goliat model.\n" \
            "Syntax:\n" \
            " "+green("generate-model <local-opts> <model-name>\n")+\
            " "+yellow("-d, --dump       ")+"   - dump to standard output\n" \
            " "+yellow("-l, --list       ")+"   - show a list of " \
            "available model at current schema\n" \
            " "+yellow("--verbose        ")+"   - run in verbose mode\n"


class CmdGenerateAll(Command):
    def __init__(self):
        self._default_opts={ 'verbose' : False, 'dump' : False }
        self._valid_opts=['-v', '--verbose', '-d', '--dump']

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
            elif x in ['-d', '--dump']:
                opts['dump']=True
            elif x.startswith('-') and x not in self._valid_opts:
                continue;
            else:
                continue

        if need_help:
            print self.long_help()
            sys.exit(-1)

        return opts

    def perform(self, args):
        opts=self.parse_args(args)
        try:
            _schema=Schema('config/schema.yaml')
            _schema.fix_tables()
        except TypeError:
            print red('The schema is not defined.')
            sys.exit(-1)
        gen=Generator(opts['verbose'])
        for model_name in _schema.get_tables_list():
            print '\n'+bold('Generating {0} model...'.format(model_name))
            templates=gen.create_b(model_name, _schema.find_table(model_name))
            if opts['dump']:
                print '\napplication/model/base/{0}Base.py'.format(
                    templates['base'][0])
                print templates['base'][1]
                if templates.get('rel')!=None:
                    for rel in templates['rel']:
                        print '\n\napplication/model/relation/{0}.py'.format(
                            rel[0])
                        print rel[1]
            else :
                gen.write_base_model(templates['base'][0],
                    templates['base'][1])
                if templates.get('rel')!=None:
                    for rel in templates['rel']:
                        gen.write_relation(rel[0], rel[1])

            print bold('Model {0} created successfully.'.format(model_name))

    def short_help(self):
        return green("<local-opts> ")+"- generate all Goliat models following" \
            " the schema.yaml file (generate --help for detailed help)"

    def long_help(self):
        return "Crate a full schema Goliat model.\n" \
            "Syntax:\n" \
            " "+green("generate-model <local-opts>\n")+\
            " "+yellow("-d, --dump       ")+"   - dump to standard output\n" \
            " "+yellow("--verbose        ")+"   - run in verbose mode\n"

_known_commands={
    'generate-model'    : CmdGenerate(),
    'generate-all'       : CmdGenerateAll()
}

_short_commands={
    'g' : 'generate-model',
    'a' : 'generate-all',
}

def model_list():
    """Return a list of available models at current schema"""
    try:
        _schema=Schema('config/schema.yaml')
        for table in _schema.get_tables_list():
            print brown(table)
    except TypeError:
        print red('Schema is not defined.')

def check_model(model_name):
    """Checks if a model given by model name exists at the current schema"""
    if not len(model_name):
        return False

    _schema=Schema('config/schema.yaml')
    if not model_name in _schema.get_tables_list():
        return False

    return True


def print_usage():
    """Print full usage information for this tool"""
    short_cmds=build_reverse_map(_short_commands)

    print 'Usage: goliat model command <local opts>\n' \
    'where command(short) is one of\n'
    keys=_known_commands.keys()
    keys.sort()
    for x in keys:
        print ' '+x+'('+green(short_cmds[x])+') '+\
        _known_commands[x].short_help()

def print_version():
    """Print the version of this tool"""
    print bold('Model Tool v{0} - Goliat Model Manager\n'.format(
        _version[1]))+bold('Copyright (C) 2010 Open Phoenix IT SCA\n')+\
    bold('Author(s): Oscar Campos Ruiz')

def parse_args(args):
    """Parse tool specific arguments.
        
    Arguments are on the form goliat 
    model <tool-specific> [command] <command-specific>
    This method will only parse the <tool-specific> bit.
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
            if x not in ['model']: local_opts.append(x)

    if not command and showhelp:
        print_usage()
        sys.exit(0)

    return (command, local_opts)
