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

    def view(self, model, controller):
        """Perform read CRUD action."""
        def cb_find(results):
            return results.all().addCallback(cb_sendback)

        def cb_sendback(results):
            ret=list()
            for row in results:
                ret.append(self._parse_result_with_schema(row,
                    self.get_model_info(model)[0]))
            controller._sendback(ret)

        if _cfg.get_config('Goliat')['Project']['tos']:
            return model.store.find(model).addCallback(cb_find)
        else:
            return cb_sendback(model.store.find(model))

    def get(self, id, model, controller):
        """Perform read CRUD action."""
        def cb_sendback(result):
            if result==None:
                self._errback('ID {0} doesn\'t exists on {1} table'.format(
                    id, model.__storm_table__), controller)
                return
            data=self._parse_result_with_schema(result,
                    self.get_model_info(model)[0])
            controller._sendback({
                'success' : True,
                'data' : data
            })

        if id=='url':
            controller._sendback({
                'success' : True,
                'data' : { 'url' : model.get_register_url() }
            })

            return

        if _cfg.get_config('Goliat')['Project']['tos']:
            return model.store.get(model, id).addCallback(cb_sendback)
        else:
            return cb_sendback(model.store.get(model, id))

    def create(self, obj, model, controller):
        """Perform create CRUD action."""
        def cb_sendback(ign):
            model.store.commit()
            controller._sendback({
                'success' : True
            })

        def cb_create(row):
            return model.store.flush().addCallback(cb_sendback, row)

        if _cfg.get_config('Goliat')['Project']['tos']:
            return model.store.add(obj).addCallback(cb_sendback)
        else:
            return cb_sendback(model.store.add(obj))

    def update(self, obj, model, controller):
        """Perform update CRUD action."""
        def cb_sendback(row):
            data=self._parse_result_with_schema(row,
                self.get_model_info(model)[0])
            controller._sendback({
                'success' : True,
                'data' : data
            })

        def cb_get(ign, id):
            return model.store.get(model, id).addCallback(cb_sendback)

        def cb_update(newobj):
            for k, v in obj.iteritems():
                if k=='id':
                    continue
                newobj.__setattr__(k, v)
            return model.store.commit().addCallback(cb_get, newobj.id)

        if _cfg.get_config('Goliat')['Project']['tos']:
            return model.store.get(model, obj['id']).addCallback(cb_update)
        else:
            newobj=model.store.get(model, obj['id'])
            for k, v in obj.iteritems():
                if k=='id':
                    continue
                newobj.__setattr__(k, v)
            model.store.commit()
            return cb_sendback(newobj)

    def destroy(self, id, model, controller):
        """Perform destroy CRUD action."""
        def cb_sendback(ign):
            controller._sendback({
                'success' : True,
                'data' : {}
            })

        def cb_remove(row):
            if row==None:
                self._errback('ID {0} doesn\'t exists on {1} table'.format(
                    id, model.__storm_table__), controller)
                return
            return model.store.remove(row).addCallback(cb_sendback)

        if _cfg.get_config('Goliat')['Project']['tos']:
            return model.store.get(model, id).addCallback(cb_remove)
        else:
            row=model.store.get(model, id)
            if row==None:
                self._errback('ID {0} doesn\'t exists on {1} table'.format(
                        id, model.__storm_table__), controller)
                return
            return cb_sendback(model.store.remove(row))

    def search(self, model, controller, *args, **kwargs):
        """Perform a database search using store find."""
        def cb_sendback(results):
            ret=list()
            for row in results:
                ret.append(self._parse_result_with_schema(row,
                    self.get_model_info(model)[0]))
            controller._sendback(ret)

        def cb_find(results):
            return results.all().addCallback(cb_sendback)

        if _cfg.get_config('Goliat')['Project']['tos']:
            return model.store.find(model, *args, **kwargs).addCallback(
                    cb_find).addErrback(self._errback, controller)
        else:
            try:
                result=model.store.find(model, *args, **kwargs)
                return cb_sendback(result)
            except ProgrammingError, e:
                model.store.commit()
                return self._errback('{0}'.format(e[0]), controller)

    def generate_object(self, ins, obj):
        """Generated an ins object with obj config."""
        for key, value in obj.iteritems():
            ins.__setattr__(key, value)

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
            if field.get('relation')!=None:
                continue
            ret[field['name']]=row.__getattribute__(field['name'])

        return ret