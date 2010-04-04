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
import platform, subprocess

debian_based = ['ubuntu', 'max', 'guadalinex', 'linex', 'knoppix', 'molinux']
redhat_based = [ 'fedora', 'centos' ]

def tacFile(installPath, options):
    pass

def mainJsFile(installPath, options):
    pass

def projectFile(installPath, options):
    pass

def initFile(installPath, options):
    """Return the correct Init file for the current distribution"""
    try:
        distro = platform.linux_distribution()[0].split(' ')[0].lower()
    except AttributeError:
        distro = platform.dist()[0].split(' ')[0].lower()
    
    init = ''
    if distro == 'gentoo':
        # Target distribution is Gentoo System
        init = "TODO"
    elif distro in debian_based or distro == 'debian':
        # Target distribution is Debian or Debian based
        init =  "TODO" 
    elif distro == "suse" or distro == "opensuse":
        # Target distribution is SuSE or openSuSE
        init = "TODO"
    
    return init

def rcUpdate(distro=None, app_name=None, add=True):
    """Enable a distro init script"""     
    if distro is None or app_name is None:
        return
    
    # SuSE and openSuSE 
    if distro == "suse" or distro == "opensuse":
        try:
            if add:
                if subprocess.call(["innserv", "/etc/init.d/{0}"]) == 0:
                    return True
            else:
                if subprocess.call(["innserv", "-r", "/etc/init.d/{0}"]) == 0:
                    return True
        except OSError:
            pass
    # Debian and some other Debian Based 
    elif distro == "debian" or distro in debian_based:
        try:
            if add:
                if subprocess.call(["update-rc.d", app_name, "defaults"]) == 0:
                    return True
            else:
                # Debian and Debian based distro check if the service script exists already on /etc/init.d
                # We will pass the -r option to the update-rc.d command to force the update
                if subprocess.call(["update-rc.d", "-f", app_name, "remove", "defaults" ]) == 0:
                    return True
        except OSError:
            pass
    # Gentoo
    elif distro == "gentoo":
        try:
            if add:
                if subprocess.call(["rc-config", "add", app_name, "default"]) == 0:
                    return True
            else:
                if subprocess.call(["rc-config", "delete", app_name, "default"]) == 0:
                    return True
        except OSError:
            pass       
    elif distro == "redhat" or distro in redhat_based:
        try:
            if add:
                if subprocess.call(["chkconfig", "--add", app_name]) == 0:
                    return True
            else:
                if subprocess.call(["chkconfig", "--del", app_name]) == 0:
                    return True
        except OSError:
            pass
    else:
        pass     
        
    return False
            
        
