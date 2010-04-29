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
# $id goliat/utils/config.py created on 05/04/2010 05:39:33 by damnwidget $
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
from ConfigParser import SafeConfigParser, RawConfigParser, \
    MissingSectionHeaderError
from goliat.utils.borg import Borg
from goliat.utils.apply import Apply
import os

class ConfigManagerException(Exception):
    pass

class ConfigManager(Borg):
    """Goliat Config File Reader and Writer
    
    Goliat implements a very simple INI files reader to load confiuration from
    files on disk. 
    """

    _config_files={}

    def __init__(self):
        Borg.__init__(self)

    def load_config(self, config_name, file_name, raw=False, config={}):
        if config_name not in self._config_files:
            self._config_files[config_name]={ 'file' : file_name }
        else:
            if self._config_files[config_name]['file']!=file_name \
            and os.path.exists(file_name):
                self._config_files[config_name]['file']=file_name

        try:
            if raw:
                self._process_raw_config_file(config_name, RawConfigParser(),
                    config)
            else:
                self._process_config_file(config_name, SafeConfigParser(),
                    config)

            return True
        except MissingSectionHeaderError:
            return False
        except ConfigManagerException:
            return False

    def reload(self, config_name, raw=False):
        if config_name in self._config_files:
            self.load_config(config_name,
                self._config_files[config_name]['file'], raw)

    def get_config(self, config_name):
        if config_name in self._config_files:
            return self._config_files[config_name]

        return None

    def _process_config_file(self, config_name, cp, config):
        self._config_files[config_name]=Apply(
            self._config_files[config_name], config)
        cp.read(self._config_files[config_name]['file'])
        if 'Goliat' not in cp.sections():
            raise ConfigManagerException('{0} is not a Goliat config file'
                .format(self._config_files[config_name]['file']))
        for s in cp.sections():
            self._config_files[config_name][s]={}
            for o in cp.options(s):
                self._config_files[config_name][s][o]=cp.get(s, o)

    def _process_raw_config_file(self, config_name, rp, config):
        self._config_files[config_name]=Apply(self._config_files[config_name],
            config)
        rp.read(self._config_files[config_name]['file'])
        if 'Goliat' not in rp.sections():
            raise ConfigManagerException('{0} is not a Goliat config file'
                .format(self._config_files[config_name]['file']))
        for s in rp.sections():
            if not s in self._config_files[config_name]:
                self._config_files[config_name][s]={}
            for o in rp.options(s):
                # From more special to more general
                try:
                    self._config_files[config_name][s][o]=rp.getboolean(s, o)
                except ValueError:
                    try:
                        self._config_files[config_name][s][o]=rp.getint(s, o)
                    except ValueError:
                        try:
                            self._config_files[config_name][s][o]=\
                                rp.getfloat(s, o)
                        except ValueError:
                            self._config_files[config_name][s][o]=rp.get(s, o)

    @staticmethod
    def write_config(config):
        """Writes a config to a file"""
        cp=SafeConfigParser()
        for section, options in config.iteritems():
            if section is not 'file' and section is not 'service':
                cp.add_section(section)
                for key, value in options.iteritems():
                    cp.set(section, key, str(value))
        cp.write(open(config['file'], 'w'))

