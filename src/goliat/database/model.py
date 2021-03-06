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
# $id goliat/database/Model.py created on 06/05/2010 19:15:14 by damnwidget $
'''
Created on 06/05/2010 19:15:14

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary: Perform general model actions.
@version: 0.1
'''
from storm.exceptions import ProgrammingError
from twisted.internet import defer
from goliat.utils.borg import Borg
from goliat.database import Database
from goliat.utils import config

_cfg=config.ConfigManager()

class Model(Borg):
    """Convenience class for Models."""

    def __init__(self):
        super(Model, self).__init__()
        self._schema=Database().get_schema()

    def get_model_info(self, model):
        """Returns a dict containing the model scheme information."""
        return (self._schema.get_model_schema(model.__storm_table__),
                self._schema.get_model_view(model.__storm_table__))

    def view(self, model):
        """Perform read CRUD action."""

        def cb_find(results):
            return results.all().addCallback(cb_order)

        def cb_order(results):
            ret=[]
            for row in results:
                ret.append(self._parse_result_with_schema(row,
                    self.get_model_info(model)[0]))
            return {'success' : True, 'data' : ret}

        if _cfg.get_config('Goliat')['Project']['tos']:
            return model.store.find(model).addCallback(cb_find)
        else:
            result=cb_order(model.store.find(model))
            return defer.succeed({'success' : True, 'data' : result})

    def get(self, id, model):
        """Perform read CRUD action."""

        def cb_order(result):
            if not result:
                return {
                    'success' : False,
                    'message' : 'ID {0} doesn\'t exists on {1} table'.format(
                    id, model.__storm_table__)
                }
            data=self._parse_result_with_schema(result,
                self.get_model_info(model)[0])
            return {'success' : True, 'data' : data}

        if id=='url':
            return {
                'success' : True,
                'data' : {
                    'url' : model.get_register_url()
                }
            }

        if _cfg.get_config('Goliat')['Project']['tos']:
            return model.store.get(model, id).addCallback(cb_order)
        else:
            result=cb_order(model.store.get(model, id))
            return defer.succeed(result)

    def create(self, obj, model, data):
        """Perform create CRUD action."""

        def cb_sendback(result):
            data['id']=obj.id
            return {
                'success' : True,
                'message' : 'Created record',
                'data' : data
            }

        if _cfg.get_config('Goliat')['Project']['tos']:
            return model.store.add(obj).addCallback(
                lambda ign: model.store.commit()).addCallback(cb_sendback)
        else:
            result=model.store.add(obj)
            model.store.commit()
            return defer.succeed({'success' : True})

    def update(self, model, data):
        """Perform update CRUD action."""

        def cb_sendback(result):
            return {'success' : True}

        def cb_update(result):
            for k, v in data.iteritems():
                if k!='id':
                    result.__setattr__(k, v)
            return model.store.commit().addCallback(cb_sendback)

        if _cfg.get_config('Goliat')['Project']['tos']:
            return model.store.get(model, data['id']).addCallback(cb_update)
        else:
            newobj=model.store.get(model, data['id'])
            for k, v in data.iteritems():
                if k is not 'id':
                    newobj.setattr(k, v)
            model.store.commit()
            return defer.succeed({'success' : True})

    def destroy(self, id, model):
        """Perform destroy CRUD action"""

        def cb_sendback(ign):
            model.store.commit()
            return {
                'success' : True
            }

        def cb_remove(row):
            if not row:
                return {
                    'success' : False,
                    'message' : 'ID {0} doesn\'t exists on {1} table'.format(
                        id, model.__storm_table__)
                }
            return model.store.remove(row).addCallback(cb_sendback)

        if _cfg.get_config('Goliat')['Project']['tos']:
            return model.store.get(model, id).addCallback(cb_remove)
        else:
            row=model.store.get(model, id)
            if not row:
                return {
                    'success' : False,
                    'message' : 'ID {0} doesn\'t exists on {1} table'.format(
                        id, model.__storm_table__)
                }
            return cb_sendback(model.store.remove(row))

    def search(self, model, *args, **kwargs):
        """Perform a database search using store find."""

        def cb_order(results):
            if not results:
                return {
                    'success' : False,
                    'message' : 'There is no row that match with the criteria.'
                }

            ret=[]
            for row in results:
                ret.append(self._parse_result_with_schema(row,
                    self.get_model_info(model)[0]))

            return {'success' : True, 'data' : ret}

        def cb_find(results):
            return results.all().addCallback(cb_order)

        if _cfg.get_config('Goliat')['Project']['tos']:
            return model.store.find(model, *args, **kwargs).addCallback(cb_find)
        else:
            try:
                result=cb_order(model.store.find(model, *args, **kwargs))
                return defer.succeed(result)
            except ProgrammingError, e:
                model.store.commit()
                return {
                    'success' : False,
                    'message' : '{0}'.format(e[0])
                }

    def generate_object(self, ins, obj):
        """Generated an ins object with obj config."""
        for key, value in obj.iteritems():
            ins.__setattr__(key, self._parse_type(key, value, ins))

        return ins

    def is_valid_object(self, object, model):
        """Returns true if an object is a valid object for model."""
        for key in object.keys():
            found=False
            for k in self.get_model_info(model)[0]:
                if key==k['name']:
                    found=True

            if not found:
                return (False, '{0} not found at model {1}'.format(
                        key, model.__storm_table__))

        return (True, '')

    def _errback(self, err, controller):
        """Send back an error."""
        controller._sendback({
            'success' : False,
            'error' : err
        })

    def _parse_result_with_schema(self, row, schema):
        """Parses the row result using the model schema."""
        ret=dict()
        for field in schema:
            if field.get('relation'):
                continue
            ret[field['name']]=row.__getattribute__(field['name'])

        return ret

    def _parse_type(self, key, value, ins):
        """Parses a value's type and returns it."""

        for k in self.get_model_info(ins.__class__)[0]:
            if k['name']==key:
                tp=k['config']['type']
                if tp=='bool' or tp=='boolean':
                    value=True if value=='true' else False
                elif tp=='integer' or tp=='smallint' or tp=='longint' \
                or tp=='serial' or tp=='bigserial' or tp=='real':
                    value=int(value)
                elif tp=='float' or tp=='double' or tp=='decimal':
                    value=float(value)
                else:
                    value=unicode(value.decode('utf8'))

        return value
