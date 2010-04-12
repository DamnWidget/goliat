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
# $id Goliat/src/goliat/utils/config.py created on 05/04/2010 05:39:33 by damnwidget $
'''
Created on 05/04/2010 05:39:33

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary:
@version: 0.1
'''
from ConfigParser import SafeConfigParser, RawConfigParser,\
    MissingSectionHeaderError
from goliat.utils.borg import Borg
from goliat.utils.apply import Apply
import os

class ConfigManagerException(Exception):
    pass

class ConfigManager(Borg):
    """Goliat Config File Reader and Writer
    
    Goliat implements a very simple INI files reader to load confiuration from files on disk.
    For load a new config file just 
    """
    
    _configFiles = {}            
    
    def __init__(self):
        Borg.__init__(self)
                
    def loadConfig(self, configName, fileName, raw=False, config={}):
        if configName not in self._configFiles:
            self._configFiles[configName] = { 'file' : fileName }
        else:
            if self._configFiles[configName]['file'] != fileName and os.path.exists(fileName):
                self._configFiles[configName]['file'] = fileName
        
        try:
            if raw:
                self._processRawConfigFile(configName, RawConfigParser(), config)                
            else:                                
                self._processConfigFile(configName, SafeConfigParser(), config)
            
            return True
        except MissingSectionHeaderError:
            return False     
        except ConfigManagerException:
            return False
            
    def reload(self, configName, raw=False):
        if configName in self._configFiles:
            self.loadConfig(configName, self._configFiles[configName]['file'],raw)
            
    def getConfig(self, configName):
        if configName in self._configFiles:
            return self._configFiles[configName]
        
        return None    
    
    def _processConfigFile(self, configName, cp, config):
        self._configFiles[configName] = Apply(self._configFiles[configName], config)                
        cp.read(self._configFiles[configName]['file'])        
        if 'Goliat' not in cp.sections():
            raise ConfigManagerException('{0} is not a Goliat config file'.format( self._configFiles[configName]['file'] ))                         
        for s in cp.sections():
            if not s in self._configFiles[configName]: self._configFiles[configName][s] = {}
            self._configFiles[configName][s] = {}
            for o in cp.options(s):
                self._configFiles[configName][s][o] = cp.get(s, o)
    
    def _processRawConfigFile(self, configName, rp, config):
        self._configFiles[configName] = Apply(self._configFiles[configName], config)
        rp.read(self._configFiles[configName]['file'])        
        if 'Goliat' not in rp.sections():
            raise ConfigManagerException('{0} is not a Goliat config file'.format( self._configFiles[configName]['file'] ))
        for s in rp.sections():
            if not s in self._configFiles[configName]: self._configFiles[configName][s] = {} 
            for o in rp.options(s):
                # From more special to more general
                try: 
                    self._configFiles[configName][s][o] = rp.getboolean(s, o)
                except ValueError:
                    try:
                        self._configFiles[configName][s][o] = rp.getint(s, o)
                    except ValueError:
                        try:
                            self._configFiles[configName][s][o] = rp.getfloat(s, o)
                        except ValueError:
                            self._configFiles[configName][s][o] = rp.get(s, o)
    
    @staticmethod
    def writeConfig(config):
        """Writes a config to a file"""
        cp = SafeConfigParser()
        for section, options in config.iteritems():
            if section is not 'file' and section is not 'service':
                cp.add_section(section)
                for key, value in options.iteritems():
                    cp.set(section, key, str(value))
        cp.write(open(config['file'], 'w'))
                                    
