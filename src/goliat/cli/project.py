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
# $id goliat/cli/project.py created on 03/04/2010 23:03:15 by damnwidget
'''
Created on 03/04/2010 23:03:15

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: damnwidget
@contact: oscar.campos@open-phoenix.com
@summary: Command Line Interface Project Manager
@version: 0.1
'''
import sys
import os
import fnmatch

import goliat._version as _goliat_version
import goliat.cli.utils.linux as linux
from goliat.cli import (
    Command, build_reverse_map, userquery, userchoice, userinput)
from goliat.cli.utils.output import *
from goliat.utils.apply import Apply
from goliat.utils import config


_version=('Project', '0.1.0')

class CmdCreate(Command):
    """Create a new Goliat Project"""


    def __init__(self):
        self._default_opts={
            'app_layout'    : 'two_columns',
            'app_file'      : 'goliat_application.tac',
            'app_version'   : '1.0',
            'app_desc'      : 'A new Goliat Application',
            'app_name'      : 'Goliat Application',
            'app_port'      : '9091'
        }

        self._valid_opts=['-d', '--description', '-f', '--file', '-l',
                          '--layout', '-v', '--verbose', '-p', '--port']

    def parse_args(self, args):
        opts=self._default_opts
        need_help=False
        app_name=''

        for i in xrange(len(args)):
            x=args[i]

            if x in ['-h', '--help']:
                need_help=True
                break;
            elif x in ['-d', '--description']:
                opts['app_desc']=args[i+1]
            elif x in ['-f', '--file']:
                opts['app_file']=args[i+1]
            elif x in ['-l', '--layout']:
                opts['app_layout']=args[i+1]
            elif x in ['-v', '--version']:
                opts['app_version']=args[i+1]
            elif x in ['-p', '--port']:
                opts['app_port']=args[i+1]
            elif x in ['--verbose']:
                opts['verbose']=True
            elif x.startswith('-') and x not in self._valid_opts:
                continue;
            else:
                if x not in opts.values():
                    app_name=x

        if need_help:
            print self.long_help()
            sys.exit(-1)

        return (app_name, opts)

    def perform(self, args):
        (app_name, opts)=self.parse_args(args)

        if app_name!='':
            if app_name=='project':
                print self.long_help()
                sys.exit(1)
            else:
                opts['app_name']=app_name
                opts['app_file']=app_name.lower().replace(' ', '_')+'.tac'
            print bold('\nYou are going to create a new Goliat Project on {0}'\
                ' with this options:\n'.format(os.path.abspath(os.getcwd())))
            for k, v in opts.iteritems():
                if k!='verbose':
                    print brown(k.ljust(12))+' :'+green('( ')+\
                    v.decode('utf8')+green(' )')
            if 'verbose' in opts:
                print brown('vebosity'.ljust(12))+' :'+green('( ')+\
                'yes'+green(' )')
            else:
                print brown('vebosity'.ljust(12))+' :'+green('( ')+\
                'no'+green(' )')
            if userquery("Would you like to create this project?")=="No":
                print '\nQuitting.'
                sys.exit(0)
            else:
                return self._create_project(opts)
        else:
            print self.long_help()
            sys.exit(-1)

    def _create_project(self, opts):
        print
        pr=Project()
        if 'verbose' in opts:
            pr.verbose()
        pr.set_name(opts['app_name'])
        pr.set_desc(opts['app_desc'])
        pr.set_port(opts['app_port'])
        pr.set_app_file(opts['app_file'])
        pr.set_app_layout(opts['app_layout'])
        pr.set_app_version(opts['app_version'])
        pr.set_log_file(opts['app_name'].lower().replace(' ', '_'))
        pr.build_template_files()
        self._write_project_files(pr)

    def _write_project_files(self, pr):
        project_dir=pr.get_name().lower().replace(' ', '_')
        try:
            # Create project directory
            if pr._verbose: print bold('Creating {0} project dir.'.format(
                os.getcwd()+'/'+project_dir))
            if os.path.exists(os.getcwd()+'/'+project_dir):
                from shutil import rmtree
                print red('\nSeems like already exists a project named {0} '\
                    'on your current path.'.format(os.getcwd()+'/'+project_dir))
                if userquery("Would you like to rename it? "\
                             "(Ctrl+c to abort)")=="Yes":
                    from random import randrange
                    rnd=str(randrange(1, 10000))
                    os.rename(os.getcwd()+'/'+project_dir, os.getcwd()+'/'+\
                        project_dir+rnd)
                    print turquoise('The old directory was saved as '\
                        '{0}.'.format(os.getcwd()+'/'+project_dir+rnd))
                else:
                    rmtree(os.getcwd()+'/'+project_dir)

            os.mkdir(os.getcwd()+'/'+project_dir)
            # Cd to the new created directory
            if pr._verbose:
                print bold('Entering {0} dir.'.format(os.getcwd()+\
                '/'+project_dir))
            os.chdir(project_dir)

            # Write tac_file template
            if pr._verbose:
                print bold('Writing {0} Twisted tac file.'.format(
                    pr.get_name()))
            self._create_tac_file(pr)
            if pr.verbose:
                print bold('Creating config directory.\nWriting schema file.')
            self._create_config_directory(pr)

            # Create application needed directories
            if pr._verbose:
                print bold('Creating application directory.\n' \
                    'Creating model directory.\nCreating controller ' \
                    'directory.\nCreating view directory.')
            self._create_application_directory()
            self._create_model_directories()
            self._create_controller_directory()
            self._create_view_directory()
            if pr._verbose:
                print bold('Creating web directory.\n' \
                    'Creating web/js directory.\n' \
                    'Creating web/media directory\n.' \
                    'Creating web/css directory.\n' \
                    'Creating services directory.' \
                    'Writing web/js/main.js UI file.'
                )
            self._create_web_directories(pr)
            self._create_services_directory()

            # Write the project config file
            if pr._verbose: print bold('Writing {0} project file.'.format(
                    pr.get_name().lower().replace(' ', '_')+'.cfg'))
            self._create_config_file(pr)

            print bold('Project Generated!')
            self._configure(pr)
        except OSError, e:
            print red(str(e))
            sys.exit(-1)

    def _create_config_file(self, pr):
        """Create the project config file."""
        fp=open(pr.get_name().lower().replace(' ', '_')+'.cfg', 'w')
        fp.write(pr.get_template('project'))
        fp.close()

    def _create_tac_file(self, pr):
        """Create the tac file."""
        fp=open(pr.get_name().lower().replace(' ', '_')+'.tac', 'w')
        fp.write(pr.get_template('tac'))
        fp.close()

    def _create_config_directory(self, pr):
        """Create the config directory."""
        os.makedirs('config')
        fp=open('config/schema.yaml', 'w')
        fp.write(pr.get_template('schema'))
        fp.close()

    def _create_application_directory(self):
        """Create the services directory."""
        os.mkdir('application')
        fp=open('application/__init__.py', 'w')
        fp.write('# Application Package')
        fp.close()

    def _create_services_directory(self):
        """Create the services directory."""
        os.mkdir('services')
        fp=open('services/__init__.py', 'w')
        fp.write('# Services for Multi Service purposes will be added to' \
            ' this directory')
        fp.close()

    def _create_view_directory(self):
        """Create the view directory."""
        os.makedirs('application/view')

    def _create_controller_directory(self):
        """Create the controller directory."""
        os.makedirs('application/controller')
        fp=open('application/controller/__init__.py', 'w')
        fp.write('# Goliat will place here the generated modules.')
        fp.close()

    def _create_model_directories(self):
        """Create the model directories."""
        os.makedirs('application/model/base')
        os.makedirs('application/model/relation')
        fp=open('application/model/__init__.py', 'w')
        fp.write('# Modules should be located on this directory')
        fp.close()
        fp=open('application/model/base/__init__.py', 'w')
        fp.write('# Goliat will place here the generated base models.')
        fp.close()
        fp=open('application/model/relation/__init__.py', 'w')
        fp.write('# Goliat will place here the generated relation models.')
        fp.close()

    def _create_web_directories(self, pr):
        """Create the web directories."""
        os.makedirs('web/js')
        os.makedirs('web/css')
        os.makedirs('web/media')
        fp=open('web/js/main.js', 'w')
        fp.write(pr.get_template('mainJs'))
        fp.close()

    def _configure(self, pr):
        cfg=CmdConfigure()
        cfg.perform({})

    def short_help(self):
        return green("<local-opts>")+" - create a new Goliat project " \
        "(create --help for detailed help)"

    def long_help(self):
        return "Crate a new Goliat project.\n" \
            "Syntax:\n"+\
            " "+green("create <local-opts> <application-name>\n")+\
            " "+yellow("-d, --description")+\
            "   - set the application description (optional)\n"+\
            " "+yellow("-f, --file       ")+\
            "   - set the application twisted tac file\n"+\
            " "+yellow("-p, --port       ")+\
            "   - set the application port\n"+\
            " "+yellow("-l, --layout     ")+\
            "   - set the application layout " \
                  "(two_columns, three_columns,\n"+\
            " "+"                 "+\
            "     two_columns_f, two_columns_h, two_columns_fh, "\
                  "three_columns_f\n"+\
            " "+"                 "+\
            "     three_columns_h, three_columns_fh, main_window, " \
                  "main_window_menu)\n"+\
            " "+yellow("--verbose        ")+\
            "   - run in verbose mode\n"+\
            " "+yellow("-v, --version    ")+\
            "   - set the application version.\n"

class CmdConfigure(Command):
    """Configure a Goliat Project"""


    def __init__(self):
        self._default_opts={
            'orbited'         : False,
            'tos'             : True,
            'debug'           : False,
            'doctype'         : 'xhtml-transitional',
            'meta_keys'       : '',
            'meta_description': None,
            'language'        : None,
            'ext_theme'       : 'xtheme-gray',
            'goliat_theme'    : 'crystal'
        }
        self._all_yes=False
        self._all_no=False

    def parse_args(self, args):
        opts=self._default_opts
        need_help=False
        need_show=False
        project=None

        for i in xrange(len(args)):
            x=args[i]

            if x in ['-h', '--help']:
                need_help=True
            elif x in ['-l', '--list']:
                self._list_projects()
                sys.exit(1)
            elif x in ['-s', '--show']:
                need_show=True
            else:
                project=x

        if need_help:
            print self.long_help()
            sys.exit(1)
        if need_show:
            self._show_project(project)
            sys.exit(0)

        return (project, opts)

    def perform(self, args):
        project, opts=self.parse_args(args)
        cfg=config.ConfigManager()
        if project==None:
            cfg=self._look_at_cur_path()
            if cfg==None:
                sys.exit(0)
            self._config_project('project', cfg, opts)
        else:
            print red('Not implemented yet.')
            sys.exit(-1)

    def _config_project(self, project, cfg, opts):
        project_file=cfg.get_config(project)['file']
        try:
            current=cfg.get_config(project)['Project']
            self._default_opts=Apply(self._default_opts, current)
        except KeyError:
            print red('{0} seems to ve an invalid Goliat Project file, ' \
                'missing \'Project\' section on file.'.format(project_file))
            sys.exit(0)

        # Application Connection Port        
        label='Would you like to change the application port? (Current: {0})' \
            .format(self._default_opts['app_port'])
        input_label='Input the application port. (> 1024)'
        if userquery(label)=="Yes":
            current['app_port']=userinput(input_label)
        else:
            current['app_port']=self._default_opts['app_port']
        # Application Layout
        label='Would you like to change your application layout? ' \
            '(Current: {0})'.format(_layouts[current['app_layout']])
        if userquery(label)=="Yes":
            current['app_layout']=\
            userchoice('Available Layouts', _layouts.keys(), _layouts.values())
        # Orbited
        label="Would you like to use Orbited COMET services on your project?" \
        " (Current: {0})".format(
            'Yes' if self._default_opts['orbited'] else 'No')
        current['orbited']=True if userquery(label)=="Yes" else False
        # Twisted on Storm
        label="Would you like to use Twisted on Storm ORM? (Current: {0})" \
            .format('Yes' if self._default_opts['tos'] else 'No')
        current['tos']=True if userquery(label)=="Yes" else False
        # JavaScript Debug or Minified files
        label="Would you like to use ExtJS and GoliatJS Debug files? " \
        "(Current: {0})".format('Yes' if self._default_opts['debug'] else 'No')
        current['debug']=True if userquery(label)=="Yes" else False
        # DocType
        label='Would you like to change your application DOCTYPE? ' \
        '(Current: {0})'.format(self._default_opts['doctype'])
        if userquery(label)=="Yes":
            current['doctype']=userchoice(
                'Available DocTypes', _docTypes.keys(), _docTypes.values())
        else:
            current['doctype']=self._default_opts['doctype']
        # Meta Keys
        current['meta_keys']=\
        userinput('Input a list of keywords separated by comma.') \
        if userquery('Would you like to change your application Meta Keywords?'\
            ' (Current: {0})'.format(
                    self._default_opts['meta_keys']))=="Yes" \
        else self._default_opts['meta_keys']
        # Meta Description
        current['meta_description']=\
        userinput('Write the meta description.') \
        if userquery('Would you like to change your application Meta ' \
            'Description? (Current: {0})'.format(
                    self._default_opts['meta_description']))=="Yes" \
        else ''
        # Language
        if userquery('Would you like to change your application language? ' \
            '(Current: {0}'.format(
                _languages[self._default_opts['language']] \
            if self._default_opts['language'] \
            else _languages[os.environ['LANG'].split('_')[0]]))=="Yes":
            current['language']=\
            userchoice(
                'Available Languages', _languages.keys(), _languages.values())
        else:
            current['language']=\
            self._default_opts['language'] \
            if self._default_opts['language'] \
            else os.environ['LANG'].split('_')[0]
        # ExtJS Theme
        current['ext_theme']=\
        userinput('Input the ExtJS theme name.') \
        if userquery('Would you like to change the ExtJS theme? (Current: {0})'
            .format(self._default_opts['ext_theme']))=="Yes" \
        else self._default_opts['ext_theme']
        # GoliatJS Theme
        current['goliat_theme']=\
        userinput('Input the Goliat theme name.') \
        if userquery('Would you like to change the Goliat theme? (Current: {0})'
            .format(self._default_opts['goliat_theme']))=="Yes" \
        else self._default_opts['goliat_theme']

        # Summary
        print bold('\nThose are your options:')
        for k, v in current.iteritems():
            print brown(k.ljust(20))+': '+green('( ')+str(v).decode('utf8')+green(' )')

        if userquery('Would you like to write the Project File and perform ' \
            'the needed changes to the application templates?')=="Yes":
            self._write_config(project)
        else:
            print '\nQuitting.'
            sys.exit(0)

    def _write_config(self, project):
        cfg=config.ConfigManager()
        config.ConfigManager.write_config(cfg.get_config(project))
        print bold('Project File writed')
        print '\nQuitting.'

    def _show_project(self, project):
        if project==None:
            cfg=self._look_at_cur_path()
            if cfg==None:
                sys.exit(0)
            self._print_project(cfg.get_config('project'))
        else:
            cfg=self._lookAtSystem(project)
            if cfg==None:
                sys.exit(0)
            self._print_project(cfg.get_config(project))


    def _look_at_cur_path(self):
        print red('No project name given, looking at current path for ' \
            'a valid project file.')
        files=[ f for f in os.listdir('.') if fnmatch.fnmatch(f, '*.cfg') ]
        match=False
        cfg=config.ConfigManager()
        for file in files:
            if cfg.load_config('project', file):
                match=True
                break;
        if match:
            return cfg
        else:
            print red('No Goliat Project files found.')
            return None

    def _look_at_system(self, project):
        try:
            sys_path='/etc/goliat/applications/'
            files=[
                f for f in os.listdir(sys_path) if fnmatch.fnmatch(f, '*.cfg')
            ]
            match=False
            cfg=config.ConfigManager()
            config_name='{0}.cfg'.format(project.lower().replace(' ', '_'))
            if config_name in files:
                if cfg.load_config(project, sys_path+config_name):
                    match=True
            if match:
                return cfg
            else:
                print red('No Goliat Project file for project {0} found.'
                    .format(project))
                return None
        except OSError, e:
            print red(e.strerror+': \''+e.filename+'\'')
            print red('No Goliat Project file for project {0} found.'
                    .format(project))
            return None

    def _list_projects(self):
        projects={}
        def info_project(data):
            ret='  '
            ret+=bold(data['Project']['app_name'].decode('utf8').ljust(30))
            ret+='Goliat v'+data['Goliat']['version'].ljust(10)
            ret+=bold('( ')
            ret+=green('running') \
            if os.path.exists('/var/run/{0}.pid'.format(
                    data['Project']['app_name'].lower().replace(' ', '_'))) \
            else red('stopped')
            ret+=bold(' )')
            return ret

        try:
            sys_path='/etc/goliat/applications/'
            files=[
                f for f in os.listdir(sys_path) if fnmatch.fnmatch(f, '*.cfg')
            ]
            cfg=config.ConfigManager()
            for file in files:
                config_name=' '.join([
                    f.capitalize() for f in file.replace('.cfg', '').split('_')
                ])
                if cfg.load_config(config_name, sys_path+file):
                    projects[config_name]=cfg.get_config(config_name)
            if len(projects):
                print green('Available Goliat Projects')
                for val in projects.values():
                    print info_project(val)
            else:
                print red('No Goliat Project files found at System Path.')
                sys.exit(0)
        except OSError, e:
            print red(e.strerror+': \''+e.filename+'\'')
            print red('No Goliat Project files found at System Path.')
            sys.exit(0)

    def _print_project(self, cfg):
        """Shows a project"""
        print green('Project {0}'.format(cfg['Project']['app_name']))
        print blue('=========================================================' \
                   '==========')
        print '  '+brown('Goliat version'.ljust(26))+cfg['Goliat']['version']
        print '  '+brown('Project name:'.ljust(26))+\
            cfg['Project']['app_name'].decode('utf8')
        print '  '+brown('Project port:'.ljust(26))+cfg['Project']['app_port']
        print '  '+brown('Project description'.ljust(26))+\
            cfg['Project']['app_desc'].decode('utf8')
        print '  '+brown('Project language'.ljust(26))+\
            _languages[cfg['Project']['language']]
        print '  '+brown('Project doctype'.ljust(26))+\
            _docTypes[cfg['Project']['doctype']]
        print '  '+brown('Project meta description'.ljust(26))+\
            cfg['Project']['meta_description'].decode('utf8')
        print '  '+brown('Project meta keywords'.ljust(26))+\
            cfg['Project']['meta_keys'].decode('utf8')
        print '  '+brown('Project ExtJS theme'.ljust(26))+\
            cfg['Project']['ext_theme']
        print '  '+brown('Project Goliat theme'.ljust(26))+\
            cfg['Project']['goliat_theme']
        print '  '+brown('Storm use Twisted'.ljust(26))+\
            (green('Yes') if cfg['Project']['tos'] else red('No'))
        print '  '+brown('Use Orbited COMET'.ljust(26))+\
            (green('Yes') if cfg['Project']['orbited'] else red('No'))
        print '  '+brown('Debug scripts used'.ljust(26))+\
            (green('Yes') if cfg['Project']['debug'] else red('No'))


    def short_help(self):
        return green("<local-opts> ")+"- configure a Goliat project " \
            "(configure --help for detailed help)"

    def long_help(self):
        return "Configure a Goliat project.\n" \
            "Syntax:\n" \
            " "+green("configure <local-opts> <application-name>\n")+\
            " If no application name is given, the tool will look " \
            "at the current path for a valid Goliat Project file.\n\n" \
            " "+yellow("-l, --list       ")+\
            "   - list available applications\n" \
            " "+yellow("-s, --show       ")+"   - show project <name>\n"


class CmdInstall(Command):
    """Install a Goliat Project"""


    def __init__(self):
        self._default_opts={
            'verbose'      : False,
            'init'         : False
        }

    def parse_args(self, args):
        opts=self._default_opts
        need_help=False

        for i in xrange(len(args)):
            x=args[i]

            if x in ['-h', '--help']:
                need_help=True
            elif x in ['-v', '--verbose']:
                opts['verbose']=True
            elif x in ['-i', '--init-script']:
                opts['init']=True

        if need_help:
            print self.long_help()
            sys.exit(-1)

        return opts

    def perform(self, args):
        if os.getuid()!=0:
            print red('You must to be root to install projects!')
            sys.exit(1)

        opts=self.parse_args(args)
        print 'Waiting for fixes, sorry'

    def short_help(self):
        return green("<local-opts> - install a Goliat project")

    def long_help(self):
        return "Install a Goliat project.\n" \
            "Note: You will run this command inside the " \
                 "project directory.\n\n" \
            "Syntax:\n"+\
            " "+green("install <local-opts>\n")+\
            " "+yellow("-v, --verbose    ")+\
            "   - run in verbose mode\n" \
            " "+yellow("-i, --init-script")+\
            "   - install the System V init scripts for {0}.\n".format(
                linux.distro)


class Project(object):
    """Goliat Projects Manager.
    
    Note that Goliat only supports those distributions:
        Gentoo and Gentoo derivates:
            Sabanyon Linux
        Debian and Debian derivates:
            Ubuntu, Knoppix, MaX, gnuLinex, Guadalinex and Molinux
        SuSE and openSuse
        RedHat and RedHat derivates:
            Fedora, CentOS
        
        For every else distribution Goliat just uses a generic System V init
        file template and will *not* auto update the rc system.     
    """


    _templates={
        'tac'       : None,
        'mainJs'    : None,
        'service'   : None,
        'project'   : None,
        'schema'    : None
    }

    _install_paths=dict()

    _options={
        'goliat_ver' : _goliat_version.version.short(),
        'project_ver': _version[1],
        'app_name'   : 'My Goliat App',
        'app_desc'   : 'My new Goliat application description',
        'app_log'    : '/var/log/goliat/my_goliat_app.log',
        'app_file'   : 'my_goliat_app.tac',
        'app_layout' : 'two_columns',
        'app_version': '1.0'
    }

    _verbose=False

    def __init__(self, options={}):
        """Constructor"""
        self._options=Apply(self._options, options)

    def get_cmd_options(self):
        return self._cmd_options

    def set_name(self, name):
        if self._verbose:
            print 'Setting project name to {0}'.format(name)
        self._options['app_name']=name

    def get_name(self):
        return self._options['app_name']

    def set_port(self, port):
        if self._verbose:
            print 'Setting project port to {0}'.format(port)
        self._options['app_port']=port

    def get_port(self):
        return self._options['app_port']

    def set_desc(self, desc):
        if self._verbose:
            print 'Setting project description to {0}'.format(desc)
        self._options['app_desc']=desc

    def get_desc(self):
        return self._options['app_desc']

    def set_log_file(self, file):
        if self._verbose:
            print 'Setting project log file to /var/log/goliat/{0}.log'.format(
                file)
        self._options['app_log']='/var/log/goliat/{0}.log'.format(file)

    def get_log_file(self):
        return self._options['app_log']

    def set_app_file(self, file):
        if self._verbose:
            print 'Setting project twisted tac file to {0}'.format(file)
        self._options['app_file']=file

    def get_app_file(self):
        return self._options['app_file']

    def set_app_layout(self, layout):
        if self._verbose:
            print 'Setting project UI layout to {0}'.format(layout)
        self._options['app_layout']=layout

    def get_app_layout(self):
        self._options['app_layout']

    def set_app_version(self, version):
        if self._verbose:
            print 'Setting project version to {0}'.format(version)
        self._options['app_version']=version

    def get_app_version(self):
        return self._options['app_version']

    def verbose(self):
        self._verbose=True

    def get_template(self, tpl_name):
        return self._templates[tpl_name]

    def build_template_files(self):
        """Setup the template for the project files"""

        # Template for twisted tac file
        self._options['app_config']=\
            self._options['app_name'].lower().replace(' ', '_')+'.cfg'
        self._templates['tac']=linux.tac_file(self._options)
        if self._verbose:
            print bold('Template for tac file generated:')

        # Template for main.js file 
        self._templates['mainJs']=linux.main_js_file(self._options)
        if self._verbose:
            print bold('Template for main UI script file generated:')

        # Template for Goliat project file
        self._templates['project']=linux.project_file(self._options)
        if self._verbose:
            print bold('Template for Goliat project file generated:')

        # Template for System V init file
        self.build_install_paths()
        self._templates['service']=\
            linux.init_file(self._install_paths, self._options)
        if self._verbose:
            print bold('Template for System V service file generated:')

        # Template for schema file
        self._templates['schema']=linux.schema_file()
        if self._verbose:
            print bold('Template for schema file generated:')


    def build_install_paths(self):
        """Setup the new project application install paths"""
        self._install_paths['share']='/var/www/goliat/app/{0}'.format(
            self._options['app_name'].lower())
        self._install_paths['service']='/etc/init.d'
        self._install_paths['config']='/etc/goliat/applications/{0}.cfg' \
            .format(self._options['app_name'].lower().replace(' ', '_'))

_known_commands={
    'create'    : CmdCreate(),
    'install'   : CmdInstall(),
    'configure' : CmdConfigure(),
    #'uninstall' : CmdUninstall()
}

_short_commands={
    'c' : 'create',
    'o' : 'configure',
    'i' : 'install',
    #'u' : 'uninstall'
}

_docTypes={
    'html-strict'        : 'HTML 4.01 Strict',
    'html-transitional'  : 'HTML 4.01 Transitional',
    'html-frameset'      : 'HTML 4.01 Frameset',
    'xhtml-strict'       : 'XHTML 1.0 Strict',
    'xhtml-transitional' : 'XHTML 1.0 Transitional',
    'xhtml-frameset'     : 'XHTML 1.0 Frameset'
}

_layouts={
    'two_columns'       : 'Two columns',
    'three_columns'     : 'Three columns',
    'two_columns_f'     : 'Two columns with footer (f)',
    'two_columns_h'     : 'Two columns with header (h)',
    'two_columns_fh'    : 'Two columns with f and h',
    'three_columns_f'   : 'Three columns with footer (f)',
    'three_columns_h'   : 'Three columns with header (h)',
    'three_columns_fh'  : 'Three columns with f and h',
    'main_window'       : 'Main window'
}

_languages={
    'bg'     :'Bulgarian',
    'cs'     :'Czech',
    'da'     :'Danish',
    'de'     :'German',
    'el'     :'Greek',
    'en'     :'English',
    'en-gb'  :'English-Great Britain',
    'en-us'  :'English-United States',
    'es'     :'Spanish',
    'es-es'  :'Spanish-Spain',
    'fi'     :'Finnish',
    'fr'     :'French',
    'fr-ca'  :'French-Quebec',
    'fr-fr'  :'French-France',
    'hr'     :'Croatian',
    'it'     :'Italian',
    'ja'     :'Japanese',
    'ko'     :'Korean',
    'nl'     :'Dutch',
    'no'     :'Norwegian',
    'pl'     :'Polish',
    'pt'     :'Portuguese',
    'ru'     :'Russian',
    'sv'     :'Swedish',
    'zh'     :'Chinese'
}



def print_usage():
    """Print full usage information for this tool"""
    short_cmds=build_reverse_map(_short_commands)

    print 'Usage: goliat project command <local opts>\n' \
    'where command(short) is one of\n'
    keys=_known_commands.keys()
    keys.sort()
    for x in keys:
        print ' '+x+'('+green(short_cmds[x])+') '+\
        _known_commands[x].short_help()

def print_version():
    """Print the version of this tool"""
    print bold('Project Tool v{0} - Goliat Project Manager\n'.format(
        _version[1]))+\
    bold('Copyright (C) 2010 Open Phoenix IT SCA\n')+\
    bold('Author(s): Oscar Campos Ruiz')

def parse_args(args):
    """Parse tool specific arguments.
        
    Arguments are on the form:
    goliat project <tool-specific> [command] <command-specific>
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
            if x not in ['project']: local_opts.append(x)

    if not command and showhelp:
        print_usage()
        sys.exit(0)

    return (command, local_opts)
