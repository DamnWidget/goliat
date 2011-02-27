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
# $id goliat/database/__init__.py created on 13/04/2010 15:53:40 by damnwidget $
'''
Created on 13/04/2010 15:53:40

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary:
@version: 0.2
'''
import sys
from storm.database import *
from psycopg2 import ProgrammingError
from storm.exceptions import OperationalError
from storm.uri import URI

from goliat.utils.borg import Borg
from goliat.database.schema import Schema, SchemaException
from goliat.cli.utils.output import *


_type_properties={
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
        'bool'          : 'TINYINT',
        'boolean'       : 'TINYINT',
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
    _db=None
    _conn=None
    _schema=None
    _fixed=False

    def __init__(self):
        super(Database, self).__init__()

        self._schema=Schema('config/schema.yaml')
        try:
            self._db=create_database(self._schema.get_properties()['uri'])
            self._initialized=True
        except:
            self._initialized=False
            raise DatabaseException("Database schema is not defined")

    def is_valid(self):
        return self._initialized

    def get_database(self):
        return self._db

    def get_schema(self):
        if not self._schema.is_fixed():
            self._schema.fix_tables()
        return self._schema

    def get_connection(self):
        if self._conn==None:
            self.connect()
        return self._conn

    def connect(self):
        if self._conn==None:
            self._conn=self._db.connect()

    def query(self, data):
        self._conn.execute(data)
        self._conn.commit()

    def create(self, script):
        drop=script.split('\n')[0]
        create=''.join(script.split('\n')[2:])
        try:
            self._conn.execute(drop)
        except ProgrammingError, e:
            print 'Drop fail: ', e[0]
            self._conn.commit()
        except OperationalError, e:
            print 'Drop fail: ', e[0]
            self._conn.commit()

        self._conn.execute(create)
        self._conn.commit()

    def drop(self, script):
        try:
            self._conn.execute(script.split('\n')[0])
        except ProgrammingError, e:
            print 'Drop fail: ', e[0]
            self._conn.commit()
        self._conn.commit()

class Generator(object):
    def __init__(self, verbose):
        self._verbose=verbose
        self._tables=[]
        self._sqlType=''
        self._dbconfig=None

    def generate_database(self):
        try:
            db=Database()
        except Exception, e:
            print '\n'+red(e[0])
            print '\nAborting'
            exit(-1)
        if self._verbose: print bold('Fixing null values on schema...')
        (success, msg)=db.get_schema().fix_tables()
        if not success:
            raise DatabaseException(msg)
        if self._verbose:
            print green('Schema fixed!')
            print bold('Retrieving database configuration...')
        self._dbconfig=db.get_schema().get_properties()
        uri=URI(self._dbconfig['uri'])
        if self._verbose:
            if uri.scheme=='sqlite':
                print bold('Trying to connect to {0} database'.format(
                    uri.database))
            else:
                print bold('Trying to connect to {0} server on {1} port {2} ' \
                    'database {3} with user {4} and passsword {5}...'.format(
                    uri.scheme.capitalize(), uri.host, uri.port,
                        uri.database, uri.username, uri.password))
        self._sqlType=uri.scheme

        try:
            for table, columns in db.get_schema().get_tables().iteritems():
                self._createTable(table, columns)
        except SchemaException:
            print 'WARNING: No tables are defined in your schema\n'+\
                'Only Goliat Users table will be generated.'


        for relation in db.get_schema().many2many():
            table=relation['table']
            cols={}
            for key in relation['keys']:
                cols[key if type(key)==str else key.keys()[0]]=\
                { 'type' : 'integer', 'required' : True, 'primaryKey' : True }
            if relation.get('fields')!=None:
                for field in relation['fields']:
                    for fname, fvalue in field.iteritems():
                        cols[fname]=fvalue
            self._createTable(table, cols, True)

        # Goliat User Table
        from goliat.session.user import user_sql_data
        self._createTable(user_sql_data.keys()[0], user_sql_data.values()[0])

    def get_database(self):
        return self._tables

    def get_sql_type(self):
        return self._sqlType

    def get_sql_quotes(self):
        if self._sqlType=='postgres': return '"'
        if self._sqlType=='mysql': return "`"
        else: return ""

    def _createTable(self, table, columns, relation=False):
        query="DROP TABLE "
        if self._sqlType=='postgres':
            query+="{0}{1}{2} CASCADE;\n\n" \
            .format(self.get_sql_quotes(), table, self.get_sql_quotes())
        if self._sqlType=='mysql':
            query+="IF EXISTS {0}{1}{2};\n\n" \
            .format(self.get_sql_quotes(), table, self.get_sql_quotes())
        if self._sqlType=='sqlite':
            query+='{0};\n\n'.format(table)
        query+="CREATE TABLE {0}{1}{2}\n" \
        .format(self.get_sql_quotes(), table, self.get_sql_quotes())
        query+="(\n"
        x=0
        if not relation:
            rcolumns=Database().get_schema().reorder_table_fields(
                Database().get_schema().find_table(table))
            for column in rcolumns:
                x+=1
                query+="    {0}{1}{2} " \
                .format(self.get_sql_quotes(), column[0], self.get_sql_quotes())
                query+=self._parse_column(column[1])
                if self._sqlType=='sqlite':
                    query+=',\n' if x<len(rcolumns) else '\n'
                else:
                    query+=',\n'
        else:
            for column in columns:
                x+=1
                if column in ['_config', '_indexes', '_relation',
                    '_parent', '_view']:
                    continue
                query+="    {0}{1}{2} " \
                .format(self.get_sql_quotes(), column, self.get_sql_quotes())
                query+=self._parse_column(columns[column])
                if self._sqlType=='sqlite':
                    query+=',\n' if x<len(columns) else '\n'
                else:
                    query+=',\n'

        # MySQL and PostgreSQL PRIMARY KEYS
        if self._sqlType in ['mysql', 'postgres']:
            query+='    PRIMARY KEY ( '
            query+=self._get_primary_keys(columns)
            query+=' )'
        if self._sqlType=='mysql':
            query+="\n)Type={0};\n".format(self._dbconfig['engine']) \
            if self._dbconfig.get('engine')!=None else "\n);\n"
        else:
            query+="\n);\n"

        tb={ 'name' : table, 'script' : query }

        self._tables.append(tb)

    def _parse_column(self, data):
        ret=''
        # Common SQL stuff
        if data.get('type')!=None:
            try:
                _type=_type_properties[self._sqlType][data['type'].lower()]
            except KeyError, e:
                print red('The {0} type is not a valid type, revise ' \
                    'your yaml definition.'.format(e[0]))
                sys.exit(-1)

            size=''
            if data.get('size')!=None:
                if self._sqlType!='sqlite':
                    if self._sqlType=='postgres':
                        if _type not in ['SMALLINT', 'INT', 'BIGINT']:
                            size='({0}) '.format(data['size'])
                    else:
                        size='({0}) '.format(data['size'])
            if data.get('primaryKey')!=None:
                if self._sqlType=='postgres':
                    if _type in ['SMALLINT', 'INT']:
                        _type='serial'
                    if _type in ['BIGINT']:
                        _type='bigserial'
            ret+='{0}{1} '.format(_type, size)

        if data.get('default')!=None:
            ret+='DEFAULT '
            if type(data['default'])==bool:
                ret+='true ' if data['default'] else 'false '
            else:
                ret+='{0} '.format(data['default'])

        if data.get('required')!=None:
            ret+='NOT NULL ' if data['required'] else ''

        if data.get('autoIncrement')!=None:
            if self._sqlType=='mysql':
                ret+='AUTO_INCREMENT '
            elif self._sqlType=='sqlite':
                ret+='PRIMARY KEY'

        return ret

    def _get_primary_keys(self, columns):
        if self._sqlType=='sqlite':
            return

        columnsList=[]
        for name, property in columns.iteritems():
            if name in ['_config', '_indexes', '_relation']:
                continue
            if 'primaryKey' in property:
                columnsList.append('{0}{1}{2}'.format(
                    self.get_sql_quotes(), name, self.get_sql_quotes()))

        return ','.join(columnsList)

