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
# $id goliat/database/schema.py created on 13/04/2010 15:54:26 by damnwidget $
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
import os
import yaml

class SchemaException(Exception):
    pass

class Schema(object):
    """Goliat YAML based Schema object"""
    _schema_file=None
    _schema={}
    _fixed=False

    def __init__(self, schema_file):
        if os.path.exists(schema_file):
            self._schema_file=schema_file
        else:
            raise SchemaException('The database schema {0} doesn\'t exists.'\
                .format(schema_file))

        super(Schema, self).__init__()
        self._load_schema()

    def get_tables(self):
        """Return the schema tables"""
        try :
            tables=self._schema['database']['tables']
        except KeyError, TypeError:
            raise SchemaException('Unable to get tables on this database '\
                'schema, revise your yaml schema definition.')
        return tables

    def get_properties(self):
        """Return the schema properties"""
        try:
            properties=self._schema['database']['_properties']
        except KeyError, TypeError:
            raise SchemaException('Unable to get database _properties, revise'\
                ' your yaml schema definition.')
        return properties

    def get_column_data(self, table, column):
        """Return data from column on table"""
        try:
            properties=self._schema['database']['tables'][table][column]
        except KeyError, TypeError:
            raise SchemaException('Unable to resolve column {0} properties on'\
                ' {1} table, revise your yaml schema definition.'\
                .format(column, table))
        return properties

    def get_column_property_data(self, table, column, property):
        """Return table column attribute value"""
        try:
            data=self._schema['database']['tables'][table][column][property]
        except KeyError:
            raise SchemaException('Unable to resolve column {0} property {1} '\
                'data on {1} table, revise your yaml schema definition.'\
                .format(column, property, table))
        return data

    def set_column_property_data(self, table, column, property, data):
        """Sets table column attribute value"""
        self._schema['database']['tables'][table][column][property]=data

    def set_column_data(self, table, column, data):
        """Sets column attributes values"""
        self._schema['database']['tables'][table][column]=data

    def find_table(self, name, ordered=False):
        """Find a table on schema and return it"""
        if name=='goliat_user':
            from goliat.session.user import user_sql_data
            return user_sql_data.values()[0]
        for table, column in self.get_tables().iteritems():
            if name==table:
                return column
        return False

    def find_reverse_reference(self, table_name):
        """Find a reverse many2many reference."""
        for table, column in self.get_tables().iteritems():
            if table_name==table:
                continue
            if self.has_relation(self.find_table(table)):
                for field, rel in column['_relation'].iteritems():
                    if rel['type']!='many2many':
                        continue

                    if rel.get('reverseId')!=None:
                        if rel['foreignTable']==table_name:
                            return {
                                'field': rel['reverseId'],
                                'type' : 'many2many',
                                'foreignTable' : table,
                                'foreignKey' : rel['localKey'],
                                'localKey' : rel['foreignKey'],
                                'keys' : [ rel['keys'][1], rel['keys'][0] ]
                            }
        return None

    def get_model_parent(self, table):
        """Return the model parent for the given table."""
        tdata=self.find_table(table)
        if not tdata:
            return None

        return tdata.get('parent')

    def get_model_view(self, table):
        """Return the model view configuration."""
        tdata=self.find_table(table)
        if not tdata:
            return None

        return tdata.get('_order')

    def get_model_schema(self, table):
        """Return the model schema definition for JavaScript use."""
        tdata=self.find_table(table)
        otdata=self.reorder_table_fields(tdata)
        if not tdata:
            return None

        model_schema=[]

        for field, data in otdata:
            model_schema.append({
                'name'   : field,
                'config' : data
            })

        for field, data in tdata.iteritems():
            if field!='_relation':
                continue

            for rel_field, rel_data in data.iteritems():
                model_schema.append({
                    'name'      : rel_field,
                    'config'    : rel_data,
                    'relation'  : True
                })

        return model_schema;


    def get_tables_list(self):
        """Return a list of tables"""
        return self._schema['database']['tables'].keys()

    def has_relation(self, table):
        """Returns true if the table has an relation"""
        if table.get('_relation')!=None:
            return True

        return False

    def many2many(self):
        """Get all the many to many relations on schema"""
        relations=[]
        for table, cols in self.get_tables().iteritems():
            if self.has_relation(cols):
                for field, definition in cols['_relation'].iteritems():
                    if definition['type']!='many2many':
                        continue
                    if definition.get('foreignKey')!=None:
                        if self.find_table(definition['foreignTable'])!=False:
                            data={
                                'table' : table+'_'+definition['foreignTable'],
                                'keys'  : definition.get('keys'),
                                'fields': definition.get('fields')
                            }
                            relations.append(data)
        return relations


    def fix_tables(self):
        """Fix tables for empty types"""
        if self._fixed:
            return (True, '')
        if not len(self.get_tables()):
            return (False, 'The data tables are empty.')

        for table, columns in self.get_tables().iteritems():
            pKey=False

            for column, properties in columns.iteritems():
                if column in ['_config', '_relation', '_indexes',
                    '_order', '_parent']:
                    continue
                # Fix the '~' columns at Yaml definition
                if properties is None:
                    if column=='created_at' or column=='updated_at':
                        self.set_column_property_data(
                            table, column, type, 'timestamp')

                    if column=='id':
                        data={
                            'type'          : 'integer',
                            'required'      : True,
                            'primaryKey'    : True,
                            'autoIncrement' : True
                        }
                        self.set_column_data(table, column, data)
                        pKey=True

                    if column.endswith('_id') \
                    and len(column.split('_id')[0])==column.find('_id'):
                        fTable=self.find_table(column.split('_id')[0])
                        if fTable:
                            data={
                                'type'              : 'integer',
                                'foreignTable'      : fTable,
                                'foreignKey'        : 'id'
                            }
                            self.set_column_data(table, column, data)
                        else:
                            raise SchemaException('Unable to resolve foreign' \
                                ' table for column {0} on table {1}'.format(
                                    column, table))
                else:
                    if not isinstance(properties, dict):
                        raise SchemaException('Column {0} properties are not '\
                            'a dict, the only valid values for define columns'\
                            ' are dicts'.format(column))
                    if properties.get('primaryKey')!=None:
                        pKey=True

            if not pKey:
                data={
                    'type'          : 'integer',
                    'required'      : True,
                    'primaryKey'    : True,
                    'autoIncrement' : True
                }
                self.set_column_data(table, column, data)

        self._fixed=True

        return (True, '')

    def is_fixed(self):
        """Returns true if the database tables are fixed, elsewhere returns
        false.
        """
        return self._fixed

    def reorder_table_fields(self, table):
        """Returns a list with ordered fields for a given table."""
        newtable=list()
        for o in table['_order']['fieldsOrder']:
            for k, v in table.items():
                if k==o:
                    newtable.append((k, v))

        return newtable

    def _load_schema(self):
        """Loads a schema from file"""
        stream=file(self._schema_file, 'r')
        self._schema=yaml.load(stream)
