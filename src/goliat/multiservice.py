# -*- coding: utf-8 -*-
##
# Goliat: The Twisted and ExtJS Web Framework
# Copyright (C) 2010 - 2011 Open Phoenix IT
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
# $id goliat/multiservice.py created on 10/04/2010 13:16:47 by damnwidget $
'''
Created on 10/04/2010 13:16:47

@license: GPLv2
@copyright: © 2010 - 2011 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary:
@version: 0.2
'''
import os
import re
import goliat
import json
from twisted.application import internet
from twisted.application.service import IServiceCollection
from twisted.internet import defer
from twisted.web import resource, server, static, http

from goliat.utils.borg import Borg
from goliat.utils.config import ConfigManager

config=ConfigManager()
cfg=config.get_config('Goliat')

class MultiService(Borg):
    """Goliat multiservice.
    
    Services are defined at /services directory on project root path.         
    """
    _serviceObjects={}
    _service={}
    _application=None

    def __init__(self, application):
        Borg.__init__(self)
        self._application=application
        self._startDate=http.datetimeToString()

    def get_service(self, name):
        """Return the service given by name if any."""
        return self._service.get(name, None)

    def get_services(self):
        """Return all the services."""
        return self._service

    def get_start_date(self):
        """Return the main application start date"""
        return self._startDate;

    def register_service(self, name):
        """Register a service"""
        self._serviceObjects[name]=Service(name)
        self._serviceObjects[name].load()

    def register_new_services(self):
        """Register new services found at /services application directory."""
        def _exploreServices():
            """Explores the module path directory and returns 
            a tuple with filenames."""
            try:
                files=os.listdir('services')
                pattern=re.compile('[^_?]\.py$', re.IGNORECASE)
                files=filter(pattern.search, files)
                return files
            except OSError:
                return list()

        for file in  _exploreServices():
            self.register_service(file)

        for name, obj in self._serviceObjects.iteritems():
            print 'Registering service {0} on port {1}...'.format(
                name, obj.get_port())
            if hasattr(obj, 'get_service'):
                self._service[name]=obj.get_service().get_service()
            else:
                self._service[name]=internet.TCPServer(obj.get_port(),
                    obj.get_factory())
            self._service[name].setName(name)
            self._service[name].setServiceParent(self._application)

    def create_service_admin_page(self):
        """Create the services admin page."""
        web_admin_root=resource.Resource()
        web_admin_root.putChild('', ServiceAdminPage(self._application))
        web_admin_root.putChild('extjs', static.File(os.path.dirname(
            goliat.__file__)+'/static/extjs'))
        web_admin_root.putChild('goliat', static.File(os.path.dirname(
            goliat.__file__)+'/static'))
        web_admin_root.putChild('web', static.File(os.path.dirname(
            goliat.__file__)+'/web'))
        web_admin_root.putChild('login', LoginRequest())
        web_admin_root.putChild('logout', LogoutRequest())
        web_admin_root.putChild('list', ListServices(self._application))
        web_admin_root.putChild('start', StartService(self._application))
        web_admin_root.putChild('stop', StopService(self._application))
        web_admin_root.putChild('check_sess', CheckSession())
        webAdminService=internet.TCPServer(cfg['Project']['admin_port'],
            server.Site(web_admin_root))
        webAdminService.setName("WebAdmin")
        webAdminService.setServiceParent(self._application)


class Service(object):
    _name='Service'
    _description=''
    _port=0
    _activation=http.datetimeToString()
    _object=None
    _loaded=False

    def __init__(self, name):
        super(Service, self).__init__()
        self._name=name.replace('.py', '')

    def load(self):
        if self._loaded: return

        _serviceName="services.{0}".format(self._name)
        _objList=[self._name]
        _tempModule=__import__(_serviceName, globals(), locals(), _objList)
        # We need an instance, not a class
        self._object=getattr(_tempModule, _objList[0])()
        self._description=self._object.get_description()
        self._port=self._object.get_port()
        self._loaded=True

    def is_loaded(self):
        return self._loaded

    def get_name(self):
        return self._name

    def get_service(self):
        return self._object

    def get_port(self):
        return self._port

    def get_description(self):
        return self._description

    def get_activation(self):
        return self._activation


class ServiceAdminPage(resource.Resource):
    def __init__(self, app):
        self.app=app

    def getChild(self, path, request):
        if path=='' or path==None or path=='index' or path=='app':
            return self

        return resource.Resource.getChild(self, path, request)

    def render_GET(self, request):
        request.write(
            """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0Transitional//EN"
            "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> 
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"> 
    <head> 
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> 
        <meta name="generator" content="Goliat Web Application Framework 
        version 0.1.0" /> 
        <meta name="description" content="Goliat 0.1.0 is a Webframework over
        Twsited, Orbited and Storm using ExtJS and OpenPhoenixJS as GUI
         enhancement. Goliat has been developed by Open Phoenix IT SCA." /> 
        <meta name="language" content="{0}" />         
        <link rel="shortcut icon" href="media/favicon.ico" /> 
        <link rel="stylesheet" href="/extjs/resources/css/ext-all.css" 
        type="text/css" /> 
        <link rel="stylesheet" href="/extjs/resources/css/xtheme-gray.css" 
        type="text/css" /> 
        <link rel="stylesheet" href="/goliat/resources/css/crystal.css" 
        type="text/css" /> 
        <script type="text/javascript" characterSet="utf-8" 
        src="/extjs/adapter/ext/ext-base.js"></script> 
        <script type="text/javascript" characterSet="utf-8" 
        src="/extjs/ext-all.js"></script> 
        <script type="text/javascript" characterSet="utf-8" 
        src="/goliat/js/goliat-min.js"></script>
        <!-- <script type="text/javascript" characterSet="utf-8" 
        src="/goliat/js/Loader.js"></script>
        <script type="text/javascript" characterSet="utf-8">
            var goliat_loader = new Goliat.Loader();
            goliat_loader.loadComponents();
        </script> -->         
        <script type="text/javascript" characterSet="utf-8" src="/web/main.js">
        </script>
        <script type="text/javascript" characterSet="utf-8" 
        src="/web/ServicesManager.js"></script>        
        <script type="text/javascript" characterSet="utf-8" 
        src="/web/adminservices/ServiceList.js"></script>
        <script type="text/javascript" characterSet="utf-8" 
        src="/web/adminservices/ServiceForm.js"></script>
        <script type="text/javascript" characterSet="utf-8" 
        src="/web/adminservices/LoginWindow.js"></script>
        <title>Goliat {1} :: Web Admin Services</title> 
    </head> 
</html>
        """.format(os.environ['LANG'].split('_')[0], goliat.version.short()))

        return ''

class StartService(resource.Resource):
    def __init__(self, app):
        self.app=app
        self.serviceName=None
        self.srv=None

    def render_POST(self, request):
        ms=MultiService(self.app)
        config=ConfigManager()
        self.serviceName=request.args.get('name', None)
        for srv in IServiceCollection(self.app):
            if not srv.running and srv.name==self.serviceName[0]:
                start=defer.maybeDeferred(srv.startService)
                self.srv=srv

        if start!=None:
            start.addCallback(self._success, request)
            start.addErrback(self._fail, self.srv, request)

            return server.NOT_DONE_YET
        if ms.get_service(self.serviceName[0])!=None:
            port=ms.get_service(self.serviceName[0]).get_port()
        else:
            port=cfg['Project']['app_port']
        return json.dumps({
            'success' : True, 'name' : self.serviceName[0], 'port' : port
        })

    def _success(self, results, request):
        ms=MultiService(self.app)
        if ms.get_service(self.serviceName[0])!=None:
            port=ms.get_service(self.serviceName[0]).get_port()
        else:
            port=cfg['Project']['app_port']
        request.write(json.dumps({
            'success' : True, 'name' : self.serviceName[0], 'port' : port
        }))
        request.finish()

    def _fail(self, results, srv, request):
        srv.stopService()
        ms=MultiService(self.app)
        if ms.get_service(self.serviceName[0])!=None:
            port=ms.get_service(self.serviceName[0]).get_port()
        else:
            port=cfg['Project']['app_port']
        request.write(json.dumps({
            'success' : False, 'name' : self.serviceName[0], 'port' : port,
            'error' : str(results).replace('\n', '<br />')
        }))
        request.finish()


class StopService(resource.Resource):
    def __init__(self, app):
        self.app=app
        self.serviceName=None
        self.srv=None

    def render_POST(self, request):
        self.serviceName=request.args.get('name', None)
        for srv in IServiceCollection(self.app):
            if srv.running and srv.name==self.serviceName[0]:
                self.srv=srv
                stop=defer.maybeDeferred(srv.stopService)

        if stop!=None:
            stop.addCallback(self._success, request)
            stop.addErrback(self._fail, self.srv, request)

            return server.NOT_DONE_YET

        return json.dumps({ 'success' : True, 'name' : self.serviceName[0] })

    def _success(self, results, request):
        request.write(json.dumps({
            'success' : True, 'name' : self.serviceName[0]
        }))
        request.finish()

    def _fail(self, results, srv, request):
        srv.stopService()
        request.write(json.dumps({
            'success' : False, 'name' : self.serviceName[0],
            'error' : str(results)
        }))
        request.finish()

class LoginRequest(resource.Resource):
    def render_POST(self, request):
        if cfg['Project']['admin']==request.args['user'][0] \
        and cfg['Project']['password']==request.args['password'][0]:
            return json.dumps({
                'success': True, 'session': request.getSession().uid
            })

        return json.dumps({ 'success': False })

class LogoutRequest(resource.Resource):
    def render_POST(self, request):
        request.getSession().expire();
        return json.dumps({ 'success': True })

class ListServices(resource.Resource):
    def __init__(self, app):
        self.app=app

    def render_GET(self, request):

        _sys_services=[]
        ms=MultiService(self.app)
        desc=act=''
        for srv in IServiceCollection(self.app):
            if srv.name=="WebAdmin": continue
            if srv.name=='{0}'.format(cfg['Project']['app_name']+' Application'):
                desc='''Main web application service.

{0}'''.format(cfg['Project']['app_desc'])
                act=ms.get_start_date()

            service={ 'name' : srv.name, 'running' : srv.running,
                     'description' : desc, 'activation' : act }
            _sys_services.append(service)

        for srv in _sys_services:
            if srv in ms.get_services().keys():
                srv['description']=ms.get_service(srv).get_description()
                srv['activation']=ms.get_service(srv).get_activation()

        return json.dumps(_sys_services)

class CheckSession(resource.Resource):
    def render_GET(self, request):
        return json.dumps({
            'success' : request.getSession().uid==request.args.get('code')
        })
