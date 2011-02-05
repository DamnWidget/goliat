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
# $id goliat/webserver/gresource.py created on 05/07/2010 16:23:42 by damnwidget $
'''
Created on 05/07/2010 16:23:42

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary:
@version: 0.1
'''
from twisted.web import resource
import json

from goliat.template import TemplateManager
from goliat.webserver.asyncjson import AsyncJSON
from goliat.environment import get_environment, set_environment

class GResource(resource.Resource):
    """
    Goliat Resource Class
    """

    def __init__(self):
        self.tplmgr=TemplateManager()
        resource.Resource.__init__(self)

    def getChild(self, name, request):
        if hasattr(self, name):
            return self
        return resource.Resource.getChild(self, name, request)

    def render(self, request):
        """
        The Goliat Resource render method.
        """
        kwargs={}
        # Environment
        if 'env' in request.args:
            set_environment(request.args.get('env')[0])
            del request.args['env']
        else:
            set_environment('production')

        for k, v in request.args.iteritems():
            kwargs[k]=v
        if len(request.prepath)>1:
            return getattr(self, request.prepath[1])(request, **kwargs)
        action_name=kwargs.get('action', None)
        if not action_name:
            return resource.Resource.render(self, request)
        action=getattr(self, action_name[0], None)
        if not action:
            return resource.Resource.render(self, request)
        return action(request, **kwargs)

    def senderrback(self, request, error):
        """
        Send back an error to the browser.
        """
        request.write(json.dumps({
            'success' : False,
            'message' : error['message'],
            'error'   : error['number']
        }))
        request.finish()

    def sendback(self, request, result):
        """
        Send back a result to the browser.
        """
        d=AsyncJSON(result).begin(request)
        d.addCallback(lambda ignored: request.finish())
