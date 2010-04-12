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
# $id Goliat/src/goliat/utils/linux.py created on 04/04/2010 01:54:45 by damnwidget
from _xmlplus.xpath.BuiltInExtFunctions import join, split
'''
Created on 04/04/2010 01:54:45

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: damnwidget
@contact: oscar.campos@open-phoenix.com
@summary: Linux distribution tools
@version: 0.1
'''
import platform
from subprocess import Popen, PIPE
from string import Template 
from goliat.template import TemplateManager

debian_based = [ 'ubuntu', 'max', 'guadalinex', 'linex', 'knoppix' ]
redhat_based = [ 'fedora', 'centos' ]
suse_based = [ 'openSuSE' ]
gentoo_based = [ 'sabanyon' ]

supported_distros = [ 'gentoo', 'debian', 'redhat', 'fedora' ]

try:
    distro = platform.linux_distribution()[0].split(' ')[0].lower()
except:
    distro = platform.dist()[0].split(' ')[0].lower()

real_distro = distro

if real_distro not in supported_distros: distro = 'generic'
if real_distro in debian_based: distro = 'debian'
if real_distro in redhat_based: distro = 'redhat'
if real_distro in suse_based: distro = 'suse'
if real_distro in gentoo_based: distro = 'gentoo'


distro_utils = {
    'debian' :  {
        'init_script' : 'rc.scripts/debian.evoque',
        'init_update' : { 
            'add' : Template('update-rc.d ${app_name} defaults'),
            'del' : Template('update-rc.d -f ${app_name} remove defaults')
        }   
    },
    'gentoo' : {
        'init_script' : 'rc.scripts/gentoo.evoque',
        'init_update' : {
            'add' : Template('rc-config --add ${app_name} default'),
            'del' : Template('rc-config --del ${app_name} default')
        }                
    },
    'redhat' : {
        'init_script' : 'rc.scripts/fedora.evoque',
        'init_update' : {
            'add' : Template('chkconfig --add ${app_name}'),
            'del' : Template('chkconfig --del ${app_name}')
        }
    },
    'suse' : {
        'init_script' : 'rc.scripts/suse.evoque',
        'init_update' : {
            'add' : Template('innserv /etc/init.d/${app_name}'),
            'del' : Template('innserv -r /etc/init.d/${app_name}')
        }
    },
    'generic' : {
        'init_script' : 'rc.scripts/generic.evoque'        
    }
}
    
def tacFile(options):
    """Generates the Twisted tac file from temnplate"""
    mgr = TemplateManager()
    t = mgr.getSysDomain().get_template('tpl/tacFile.evoque')
    return t.evoque(
            app_name=options['app_name'],
            app_config=options['app_config']
    )

def mainJsFile(options):
    """Generates the Goliat main application JavaScript file from template"""
    mgr = TemplateManager()
    t = mgr.getSysDomain().get_template('tpl/mainJsFile.evoque')
    return t.evoque(
            app_name=options['app_name'].replace(' ', ''),
            app_version=options['app_version'],
            app_layout='Goliat.layout.'+''.join([p.capitalize() for p in options['app_layout'].split('_')])            
    )

def projectFile(options):
    """Generates the Goliat project file from template"""
    mgr = TemplateManager()
    t = mgr.getSysDomain().get_template('tpl/projectFile.evoque')
    return t.evoque(
            goliat_ver=options['goliat_ver'],
            project_ver=options['app_version'],            
            app_name=options['app_name'],
            app_desc=options['app_desc'],
            app_layout=options['app_layout'],  
            app_port=options['app_port']          
    )

def initFile(installPath, options):
    """Return the correct Init file for the current distribution."""
    mgr = TemplateManager()
    t = mgr.getSysDomain().get_template('rc.scripts/{0}.evoque'.format( distro ))
    return t.evoque(
             app_name=options['app_name'],
             app_desc=options['app_desc'],
             app_file=options['app_file'],
             app_log=options['app_log'],
             app_share=installPath['share']
    )     

def rcUpdate(app_name, add='add'):
    """Enable or diable a distro System V init script"""
    if distro == 'generic':
        return (False, 'Your distribution {0} is not supported by Goliat. A generic System V init script has been created on /etc/init.d you will add it to your runlevel manually.'.format( real_distro ))
    try:
        p = Popen(distro_utils[distro]['init_update'][add].substitute(app_name=app_name).split(' '), stdout=PIPE, stderr=PIPE)
        return (True, p.communicate())
    except OSError:
        return add(False, 'Failed to use {0} on {1} system. Seems like the command doesn\'t exists'.format(distro_utils[distro]['init_update'][add].substitute(app_name=app_name), distro))

def isSupported(distro):
    return distro in supported_distros    
