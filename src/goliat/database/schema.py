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
# $id Goliat/src/goliat/database/schema.py created on 13/04/2010 15:54:26 by damnwidget $
'''
Created on 13/04/2010 15:54:26

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary:
@version: 0.1
'''
import os, yaml

class SchemaException(Exception):
    pass

class Schema(object):
    _schemaFile = None    
    _schema = {}
    
    def __init__(self, schemaFile):
        if os.path.exists(schemaFile):
            self._schemaFile = schemaFile
        else:
            raise SchemaException('The database schema {0} doesn\'t exists.'.format( schemaFile ))             
        
        super(Schema, self).__init__()                        
        self._loadSchema()
    
    def _loadSchema(self):
        stream = file(self._schemaFile, 'r')
        self._schema = yaml.load(stream)
    
    def getTables(self):
        try : 
            tables = self._schema['database']['tables']
        except KeyError:
            raise SchemaException('Unable to get tables on this database schema, revise your yaml schema definition.')             
        return tables
    
    def getProperties(self):
        try:
            properties = self._schema['database']['_properties']
        except KeyError:
            raise SchemaException('Unable to get database _properties, revise your yaml schema definition.')            
        return properties
    
    def getColumnData(self, table, column):
        try:
            properties = self._schema['database']['tables'][table][column]
        except KeyError:
            raise SchemaException('Unable to resolve column {0} properties on {1} table, revise your yaml schema definition.'.format( column, table ))
        return properties
    
    def getColumnPropertyData(self, table, column, property):
        try:
            data = self._schema['database']['tables'][table][column][property]
        except KeyError:
            raise SchemaException('Unable to resolve column {0} property {1} data on {1} table, revise your yaml schema definition.'.format( column, property, table ))
        return data
    
    def setColumnPropertyData(self, table, column, property, data):
        self._schema['database']['tables'][table][column][property] = data
    
    def setColumnData(self, table, column, data):
        self._schema['database']['tables'][table][column] = data
    
    def findTable(self, name):
        for table, column in self.getTables().iteritems():
            if name == table or column.get('_config') != None and column['_config'].get('modName') != None and column['_config']['modName'] == name:
                return column 
            return False
