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
# $id goliat/cli/module.py created on 19/04/2010 15:05:00 by damnwidget $
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
from datetime import datetime
import sys
import os
import fnmatch

from goliat.cli import Command, build_reverse_map
from goliat.cli.utils.output import *
from goliat.model import Generator
from goliat.database.schema import Schema
from goliat.template import TemplateManager
from goliat.utils import config

_version=('Module', '0.1.0')

class CmdGenerateModule(Command):
    """Create a new Goliat model"""
    def __init__(self):
        self._default_opts={ 'verbose' : False, 'dump' : False }
        self._valid_opts=['-v', '--verbose', '-d', '--dump', '-l', \
            '--list', '-m', '--model']

    def parse_args(self, args):
        opts=self._default_opts
        need_help=False
        module_name=''

        for i in xrange(len(args)):
            x=args[i]

            if x in ['-h', '--help']:
                need_help=True
                break;
            elif x in ['-v', '--verbose']:
                opts['verbose']=True
            elif x in ['-d', '--dump']:
                opts['dump']=True
            elif x in ['-m', '--model']:
                opts['model']=args[i+1]
            elif x in ['-l', '--list']:
                model_list()
                sys.exit(1)
            elif x.startswith('-') and x not in self._valid_opts:
                continue;
            else:
                if x not in opts.values():
                    module_name=x

        if need_help:
            print self.long_help()
            sys.exit(-1)

        return (module_name, opts)

    def perform(self, args):
        cfg=self._look_at_cur_path()
        module_name, opts=self.parse_args(args)
        if not len(module_name):
            print self.long_help()
            sys.exit(-1)
        try:
            _schema=Schema('config/schema.yaml')
            _schema.fix_tables()
        except TypeError:
            print red('The schema is not defined.')
            sys.exit(-1)
        _module_model_import=''
        _module_get_schema_model=''
        _module_render_get_code="return json.dumps({'success' : False, " \
            "'error' : 'Not implemented yet.'})"
        _module_render_post_code="return json.dumps({'success' : False, " \
            "'msg' : 'Not implemented yet.'})"

        if opts.get('path')==None:
            _module_register_path='"{0}"'.format(module_name.lower())
        else:
            _module_register_path='"{0}"'.format(opts['path'])
        if opts.get('model')!=None:
            if not check_model(opts['model']):
                print red(\
                '\n{0} model does not exist at the project schema.\nUse ' \
                'module -l or module --list to show a list of available ' \
                'models.'.format(\
                    opts['model'] if len(opts['model']) else 'Noname'))
                sys.exit(0)
            gen=Generator(opts['verbose'])
            tmodel=gen.create_m(\
                opts['model'], _schema.find_table(opts['model']),
                _module_register_path)

            _module_model_import='from application.model.{0} import {1}' \
            .format(gen._generate_model_name(opts['model']),
                gen._generate_model_name(opts['model']))
            _module_get_schema_model='''def get_schema_model(self): 
        """Return the schema model %s architecture.""" 
        model_schema, model_view = %s.get_model_info() 
        if model_schema == None: 
            return json.dumps({
                "success" : False,
                "error" : "Unable to fetch a schema for model %s"
            })        
                
        return json.dumps({
            "success" : True,
            "model" : model_schema,
            "view" : model_view
        })'''%(gen._generate_model_name(opts['model']),
            gen._generate_model_name(opts['model']),
            opts['model'])
            _module_render_get_code='''_act = request.args.get('act')
        if _act != None and 'getSchemaModel' in _act:            
            return self.get_schema_model()
        elif _act != None and 'view' in _act:
            %s.view(self)
            return server.NOT_DONE_YET
        elif _act != None and 'get' in _act:
            %s.get(self)
            return server.NOT_DONE_YET
        else:
            return json.dumps(
                {'success' : False, 'error' : 'Not implemented yet.'})
            '''%(gen._generate_model_name(opts['model']),
                 gen._generate_model_name(opts['model']))
            _module_render_post_code='''_act = request.args.get('act')
        if _act != None and 'create' in _act:
            %s.create(self)
            return server.NOT_DONE_YET
        elif _act != None and 'update' in _act:
            %s.update(self)
            return server.NOT_DONE_YET
        elif _act != None and 'destroy' in _act:
            %s.destroy(self)
            return server.NOT_DONE_YET
        else:
            return json.dumps(
                {'success' : False, 'error' : 'Not implemented yet.'})
            '''%(gen._generate_model_name(opts['model']),
                gen._generate_model_name(opts['model']),
                gen._generate_model_name(opts['model']))

        print '\n'+bold('Generating {0} module...'.format(module_name))
        mgr=TemplateManager()
        t=mgr.get_sys_domain().get_template('tpl/module.evoque')
        module=t.evoque(
            module_file="application/controller/{0}".format(module_name),
            module_creation_date=datetime.now(),
            module_render_get_code=_module_render_get_code,
            module_render_post_code=_module_render_post_code,
            module_name=module_name,
            module_model_import=_module_model_import,
            module_register_path=_module_register_path,
            module_get_schema_model=_module_get_schema_model
        )
        if opts['dump']:
            if opts.get('model')!=None:
                print '\napplication/model/{0}.py'.format(tmodel['work'][0])
                print tmodel['work'][1]
            print '\napplication/controller/{0}.py'.format(module_name)
            print  module
        else :
            if opts.get('model')!=None:
                gen.write_model(tmodel['work'][0], tmodel['work'][1])
            fp=file('application/controller/{0}.py'.format(module_name), 'w')
            fp.write(module.encode('utf8'))
            fp.close()

        print bold('Module created successfully.')

    def short_help(self):
        return green("<local-opts> ")+"- generate a new Goliat module " \
            "(generate --help for detailed help)"

    def long_help(self):
        return "Crate a new Goliat module.\n\n" \
            "Syntax:\n" \
            " "+green("generate-model <local-opts> <module-name>\n")+\
            " "+yellow("-m, --model      ")+"   - model based on\n" \
            " "+yellow("-m, --path       ")+"   - register path\n" \
            " "+yellow("-d, --dump       ")+"   - dump to standard output\n" \
            " "+yellow("-l, --list       ")+"   - show a list of " \
            "available model at current schema\n" \
            " "+yellow("--verbose        ")+"   - run in verbose mode\n"

    def _look_at_cur_path(self):
        files=[ f for f in os.listdir('.') if fnmatch.fnmatch(f, '*.cfg') ]
        match=False
        cfg=config.ConfigManager()
        for file in files:
            if cfg.load_config('project', file, True):
                match=True
                break;
        if match:
            return cfg
        else:
            print red('No Goliat Project files found.')
            return None


_known_commands={
    'generate'    : CmdGenerateModule()
}

_short_commands={
    'g' : 'generate'
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

    print 'Usage: goliat module command <local opts>\n' \
    'where command(short) is one of\n'
    keys=_known_commands.keys()
    keys.sort()
    for x in keys:
        print ' '+x+'('+green(short_cmds[x])+') '+\
        _known_commands[x].short_help()

def print_version():
    """Print the version of this tool"""
    print bold('Module Tool v{0} - Goliat Module Manager\n' \
    .format(_version[1]))+\
    bold('Copyright (C) 2010 Open Phoenix IT SCA\n')+\
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
            if x not in ['module']: local_opts.append(x)

    if not command and showhelp:
        print_usage()
        sys.exit(0)

    return (command, local_opts)
