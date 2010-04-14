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
# $id Goliat/src/goliat/database/__init__.py created on 13/04/2010 15:53:40 by damnwidget $
from _xmlplus.xpath.BuiltInExtFunctions import join
'''
Created on 13/04/2010 15:53:40

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary:
@version: 0.1
'''
from storm.database import *
from goliat.utils.borg import Borg
from goliat.database.schema import Schema
from psycopg2 import ProgrammingError

_type_properties = {
    'sqlite' : {
        'bool'          : 'INTEGER',
        'boolean'       : 'INTEGER',
        'integer'       : 'INTEGER',
        'smallint'      : 'INTEGER',
        'longint'       : 'INTEGER',
        'serial'        : 'INTEGER',
        'bigserial'     : 'INTEGER',
        'real'          : 'REAL',
        'float'         : 'FLOAT',
        'double'        : 'DOUBLE',
        'decimal'       : 'TEXT',
        'unicode'       : 'TEXT',
        'varchar'       : 'VARCHAR',
        'longvarchar'   : 'TEXT',
        'rawstr'        : 'BLOB',
        'any'           : 'BLOB',
        'timestamp'     : 'TEXT',
        'date'          : 'TEXT',
        'time'          : 'TEXT',
        'timedelta'     : 'TEXT',
        'list'          : 'TEXT'        
    },
    'postgres' : {
        'bool'          : 'BOOL',
        'boolean'       : 'BOOL',
        'integer'       : 'INT',
        'smallint'      : 'SMALLINT',
        'longint'       : 'BIGINT',
        'serial'        : 'SERIAL',
        'bigserial'     : 'BIGSERIAL',
        'real'          : 'REAL',
        'float'         : 'FLOAT',
        'double'        : 'DOUBLE PRECISION',
        'decimal'       : 'DECIMAL',
        'unicode'       : 'TEXT',
        'varchar'       : 'VARCHAR',
        'longvarchar'   : 'TEXT',
        'rawstr'        : 'BYTEA',
        'any'           : 'BYTEA',
        'timestamp'     : 'TIMESTAMP',
        'date'          : 'DATE',
        'time'          : 'TIME',
        'timedelta'     : 'INTERVAL',
        'list'          : 'ARRAY[]'
    },
    'mysql' : {
        'bool'          : 'TINYINT(1)',
        'boolean'       : 'TINYINT(1)',
        'integer'       : 'INT',
        'smallint'      : 'SMALLINT',
        'longint'       : 'BIGINT',
        'serial'        : 'INT',
        'bigserial'     : 'BIGINT',
        'real'          : 'REAL',
        'float'         : 'FLOAT',
        'double'        : 'DOUBLE PRECISION',
        'decimal'       : 'DECIMAL',
        'unicode'       : 'TEXT',
        'varchar'       : 'VARCHAR',
        'longvarchar'   : 'TEXT',
        'rawstr'        : 'VARBINARY',
        'any'           : 'BINARY',
        'timestamp'     : 'TIMESTAMP',
        'date'          : 'DATE',
        'time'          : 'TIME',
        'timedelta'     : 'TEXT',
        'list'          : 'TEXT'
    }
}

class DatabaseException(Exception):
    pass

class Database(Borg):
    _db = None    
    _conn = None      
    _schema = None
    _fixed = False
        
    def __init__(self):
        super(Database, self).__init__()        
        
        self._schema = Schema('config/schema.yaml')        
        self._db = create_database(self._schema.getProperties()['uri'])        
    
    def getDatabase(self):
        return self._db    
    
    def connect(self):
        self._conn = self._db.connect()
    
    def execute(self, query):
        self._conn.execute(query)
            
    def create(self, query):
        drop = query.split('\n')[0]
        create = ''.join(query.split('\n')[2:])
        try:
            self._conn.execute(drop)
        except ProgrammingError, e:
            if 'does not exist' in e[0]:
                print 'Drop fail: ',e[0]
            else:
                raise ProgrammingError(e[0])
            self._conn.commit()            
        
        self._conn.execute(create)
        self._conn.commit()        
    
    def fixTables(self):
        if self._fixed:
            return
        if not len(self._schema.getTables()):
            return (False, 'The data tables are empty.')
        
        for table, columns in self._schema.getTables().iteritems():
            pKey = False
            
            for column, properties in columns.iteritems():
                if column in ['_config', '_behavior']:
                    continue
                # Fix the '~' columns at Yaml definition
                if properties is None:
                    if column == 'created_at' or column == 'updated_at':
                        self._schema.setColumnPropertyData(table, column, type, 'timestamp')
                    
                    if column == 'id':
                        data = {
                            'type'          : 'integer',
                            'required'      : True,
                            'primaryKey'    : True,
                            'autoIncrement' : True
                        }
                        self._schema.setColumnData(table, column, data)
                        pKey = True  
                    
                    if column.endswith('_id') and len(column.split('_id')[0]) == column.find('_id'):
                        fTable = self._schema.findTable(column.split('_id')[0])
                        if fTable:
                            data = {
                                'type'              : 'integer',
                                'foreignTable'      : fTable,
                                'foreignReference'  : 'id'
                            }
                            self._schema.setColumnData(table, column, data)
                        else:
                            raise DatabaseException('Unable to resolve foreign table for column {0} on table {1}'.format( column, table ))
                else:
                    if not isinstance(properties, dict):
                        raise DatabaseException('Column {0} properties are not a dict, the only valid values for define columns are dicts'.format( column ))                    
                    if properties.get('primaryKey') != None:
                        pKey = True
                
            if not pKey:
                data = {
                    'type'          : 'integer',
                    'required'      : True,
                    'primaryKey'    : True,
                    'autoIncrement' : True
                }
                self._schema.setColumnData(table, column, data)
        
        self._fixed = True
                             
    def getSchema(self):
        return self._schema    
    
