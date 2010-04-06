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
# $id Goliat/src/goliat/cli/project.py created on 03/04/2010 23:03:15 by damnwidget
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
import goliat._version as _goliat_version
import goliat.cli.utils.linux as linux
from goliat.cli import Command, buildReverseMap, userquery
from goliat.cli.utils.output import bold, white, turquoise, purple, red, yellow, green, blue, brown
from goliat.utils.apply import Apply
import sys, os


_version = ('Project', '0.1.0')

class CmdCreate(Command):
    """Create a new Goliat Project"""
    def __init__(self):
        self._default_opts = {
            'app_layout'    : 'two_columns',
            'app_file'      : 'goliat_application.tac',
            'app_version'   : '1.0',
            'app_desc'      : 'A new Goliat Application',
            'app_name'      : 'Goliat Application',            
        }
        
        self._valid_opts = ['-d', '--description', '-f', '--file', '-l', '--layout', '-v', '--verbose']
    
    def parseArgs(self, args):
        opts = self._default_opts
        need_help = False
        app_name = ''        
        
        for i in xrange(len(args)):
            x = args[i]
            
            if x in ['-h', '--help']:
                need_help = True
                break;
            elif x in ['-d', '--description']:
                opts['app_desc'] = args[i+1]
            elif x in ['-f', '--file']:
                opts['app_file'] = args[i+1]
            elif x in ['-l', '--layout']:
                opts['app_layout'] = args[i+1]
            elif x in ['-v', '--version']:
                opts['app_version'] = args[i+1]
            elif x in ['--verbose']:
                opts['verbose'] = True
            elif x.startswith('-') and x not in self._valid_opts:
                continue; 
            else:
                if x not in opts.values():
                    app_name = x
        
        if need_help:
            print self.longHelp()
            sys.exit(-1)            
                 
        return (app_name, opts)
    
    def perform(self, args):
        (app_name, opts) = self.parseArgs(args)
        
        if app_name != '':
            if app_name == 'project':
                print self.longHelp()
                sys.exit(1)
            else:
                opts['app_name'] = app_name
                opts['app_file'] = app_name.lower().replace(' ', '_')+'.tac'
            print bold('\nYou are going to create a new Goliat Project on {0} with this options:\n'.format( os.path.abspath(os.getcwd()) ))
            for k, v in opts.iteritems():                
                if k != 'verbose':
                    print brown(k.ljust(12)) + ' :' + green('( ') + v.decode('utf8') + green(' )')
            if 'verbose' in opts:
                print brown('vebosity'.ljust(12)) + ' :' + green('( ') + 'yes' + green(' )')
            else:
                print brown('vebosity'.ljust(12)) + ' :' + green('( ') + 'no' + green(' )')
            if userquery("Would you like to create this project?") == "No":
                print '\nQuitting.'
                sys.exit(0)
            else:
                return self._createProject(opts)
        else:
            print self.longHelp()
            sys.exit(-1)  
            
    def _createProject(self, opts):
        print
        pr = Project()
        if 'verbose' in opts:
            pr.verbose()
        pr.setName(opts['app_name'])
        pr.setDesc(opts['app_desc'])
        pr.setAppFile(opts['app_file'])
        pr.setAppLayout(opts['app_layout'])
        pr.setAppVersion(opts['app_version'])
        pr.setLogFile(opts['app_name'].lower().replace(' ','_'))
        pr.buildInstallPaths()
        pr.buildTemplateFiles()
        self._writeProjectFiles(pr)
    
    def _writeProjectFiles(self, pr):
        pass
        
    
    def shortHelp(self):
        return green("<local-opts> - create a new Goliat project (create --help for detailed help)")
    
    def longHelp(self):
        return bold("Crate a new Goliat project.") + \
            "\n" + \
            bold("Syntax:\n") + \
            " " + green("create <local-opts> <application-name>\n") + \
            " " + yellow("-d, --description") + green("   - set the application description (optional)\n") + \
            " " + yellow("-f, --file       ") + green("   - set the application twisted tac file\n") + \
            " " + yellow("-l, --layout     ") + green("   - set the application layout (two_columns, three_columns,\n") + \
            " " + "                 " + green("     two_columns_f, two_columns_h, two_columns_fh, three_columns_f\n") + \
            " " + "                 " + green("     three_columns_h, three_columns_fh, main_window, main_window_menu)\n") + \
            " " + yellow("--verbose        ") + green("   - run in verbose mode\n") + \
            " " + yellow("-v, --version    ") + green("   - set the application version.\n")


class CmdInstall(Command):
    """Install a Goliat Project"""
    def __init__(self):       
        self._default_opts = {
            'verbose'      : False,
            'init'         : False
        }
    
    def parseArgs(self, args):
        opts = self._default_opts
        need_help = False        
        
        for i in xrange(len(args)):
            x = args[i]
            
            if x in ['-h', '--help']:
                need_help = True
            elif x in ['-v', '--verbose']:
                opts['verbose'] = True
            elif x in ['-i', '--init-script']:
                opts['init'] = True                
        
        if need_help:
            print self.longHelp()
            sys.exit(-1)
        
        return opts
    
    def perform(self, args):
        if os.getuid() != 0:
            print red('You must to be root to install projects!')
            sys.exit(1)
            
        opts = self.parseArgs(args)
        print 'Not implemented yet'     
        print 'Maricuchili'   
    
    def shortHelp(self):
        return green("<local-opts> - install a Goliat project")
    
    def longHelp(self):
        return bold("Install a Goliat project.") + \
            bold("Note: You will run this command inside the project directory.\n") + \
            "\n" + \
            bold("Syntax:\n") + \
            " " + green("install <local-opts>\n") + \
            " " + yellow("-v, --verbose    ") + green("   - run in verbose mode\n") + \
            " " + yellow("-i, --init-script") + green("   - install the System V init scripts for {0}.\n".format( linux.distro ))          


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
        
        For every else distribution Goliat just uses a generic System V init file template
        and will *not* auto update the rc system.     
    """
    _templates = {
        'tacFile'       : None,
        'mainJsFile'    : None,
        'serviceFile'   : None,
        'projectFile'   : None
    }
    
    _installPaths = dict()
    
    _options = {
        'goliat_ver' : _goliat_version.version.short(),
        'project_ver': _version[1],
        'app_name'   : 'My Goliat App',
        'app_desc'   : 'My new Goliat application description',
        'app_log'    : '/var/log/goliat/my_goliat_app.log',
        'app_file'   : 'my_goliat_app.tac',
        'app_layout' : 'two_columns',
        'app_version': '1.0'
    }   
    
    _verbose = False    
    
    def __init__(self, options={}):
        """Constructor"""        
        self._options = Apply(self._options, options)                
        
    def getCmdOptions(self):
        return self._cmd_options
        
    def setName(self, name):
        if self._verbose:
            print 'Setting project name to {0}'.format( name )
        self._options['app_name'] = name
    
    def getName(self):
        return self._options['app_name']
    
    def setDesc(self, desc):
        if self._verbose:
            print 'Setting project description to {0}'.format( desc )
        self._options['app_desc'] = desc
        
    def getDesc(self):        
        return self._options['app_desc']
    
    def setLogFile(self, file):
        if self._verbose:
            print 'Setting project log file to /var/log/goliat/{0}.log'.format( file )
        self._options['app_log'] = '/var/log/goliat/{0}.log'.format( file )
    
    def getLogFile(self):
        return self._options['app_log']
    
    def setAppFile(self, file):
        if self._verbose:
            print 'Setting project twisted tac file to {0}'.format( file )
        self._options['app_file'] = file
        
    def getAppFile(self):
        return self._options['app_file']
    
    def setAppLayout(self, layout):
        if self._verbose:
            print 'Setting project UI layout to {0}'.format( layout )
        self._options['app_layout'] = layout
    
    def getAppLayout(self):
        self._options['app_layout']
    
    def setAppVersion(self, version):
        if self._verbose:
            print 'Setting project version to {0}'.format( version )
        self._options['app_version'] = version
    
    def getAppVersion(self):
        return self._options['app_version']
    
    def verbose(self):
        self._verbose = True  
    
    def buildTemplateFiles(self):
        """Setup the template for the project files"""
        
        # Template for twisted tac file
        self._templates['tacFile'] = linux.tacFile(self._options)
        if self._verbose:
            print bold('Template for tac file generated:')
            print brown(self._templates['tacFile'])
        
        # Template for main.js file 
        self._templates['mainJsFile'] = linux.mainJsFile(self._options)
        if self._verbose:
            print bold('Template for main UI script file generated:')
            print brown(self._templates['mainJsFile'])
        
        # Template for Goliat project file
        self._templates['projectFile'] = linux.projectFile(self._options)
        if self._verbose:
            print bold('Template for Goliat project file generated:')
            print brown(self._templates['projectFile']) 
        
        # Template for System V init file
        self._templates['serviceFile'] = linux.initFile(self._installPaths, self._options)
        if self._verbose:
            print bold('Template for System V service file generated:')
            print brown(self._templates['serviceFile'])
    
    def buildInstallPaths(self):
        """Setup the new project application install paths"""       
        self._installPaths['share'] = '/var/www/goliat/app/{0}'.format( self._options['app_name'].lower() )            
        self._installPaths['service'] = '/etc/init.d'
        self._installPaths['config'] = '/etc/goliat/applications/{0}.cfg'.format( self._options['app_name'].lower() )


_known_commands = {
    'create'    : CmdCreate(),
    'install'   : CmdInstall(),
    #'uninstall' : CmdUninstall()
}
    
_short_commands = {
    'c' : 'create',
    'i' : 'install',
    #'u' : 'uninstall'
}

def printUsage():
    """Print full usage information for this tool"""
    short_cmds = buildReverseMap(_short_commands)
        
    print bold('Usage: goliat project command <local opts>\n') + \
    bold('where command(short) is one of\n')
    keys = _known_commands.keys()
    keys.sort()
    for x in keys:
        print ' ' + yellow(x) + bold('(') + turquoise(short_cmds[x]) + bold(') ') + \
        green(_known_commands[x].shortHelp())
        
def printVersion():
    """Print the version of this tool"""
    print bold('Project Tool v{0} - Goliat Project Manager\n'.format( _version[1] )) + \
    bold('Copyright (C) 2010 Open Phoenix IT SCA\n') + \
    bold('Author(s): Oscar Campos Ruiz')
    
def parseArgs(args):
    """Parse tool specific arguments.
        
    Arguments are on the form goliat project <tool-specific> [command] <command-specific>
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
            local_opts.append(x)
        
    if not command and showhelp:
        printUsage()
        sys.exit(0)
        
    return (command, local_opts)
