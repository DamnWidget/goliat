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
# $id Goliat/src/goliat/multiservice.py created on 10/04/2010 13:16:47 by damnwidget $
'''
Created on 10/04/2010 13:16:47

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: damnwidget
@contact: oscar.campos@open-phoenix.com
@summary:
@version: 0.1
'''
from goliat.utils.borg import Borg
from goliat.utils.config import ConfigManager
from twisted.application import internet
from twisted.application.service import IServiceCollection
from twisted.internet import defer
from twisted.web import resource, server, static, http
from twisted.python import log
import os, re, goliat, json

config = ConfigManager()
cfg = config.getConfig('Goliat')

class MultiService(Borg):
    """Goliat multiservice.
    
    Services are defined at /services directory on project root path.         
    """
    _serviceObjects = {}
    _service = {}    
    _application = None
    
    def __init__(self, application):
        Borg.__init__(self)
        self._application = application
        self._startDate = http.datetimeToString()
    
    def getService(self, name):
        """Return the service given by name if any."""
        return self._service.get(name, None)
    
    def getServices(self):
        """Return all the services."""
        return self._service

    def getStartDate(self):
        """Return the main application start date"""
        return self._startDate;
            
    def registerService(self, name):
        """Register a service"""        
        self._serviceObjects[name] = Service(name)
    
    def registerNewServices(self):
        """Register new services found at /services application directory."""
        def _exploreServices():
            """Explores the module path directory and returns a tuple with filenames."""
            try:
                files = os.listdir('application')        
                pattern = re.compile('[^_?]\.py$', re.IGNORECASE)
                files = filter(pattern.search, files)
                return files
            except OSError:
                return list()  
        
        for file in  _exploreServices():        
            self.registerService(file)
        
        for name, obj in self._serviceObjects.iteritems():
            log.msg('Registering service {0} on port {1}...'.format( name, obj.getPort() ))
            self._service[name] = internet.TCPServer(obj.getPort(), obj.getFactory())
            self._service[name].setName(name)
            self._service[name].setServiceParent(self._application)
            self._service[name].setDescription(obj.getDescription())
    
    def createServiceAdminPage(self):
        """Create the services admin page."""
        webAdminRoot = resource.Resource()
        webAdminRoot.putChild('', ServiceAdminPage(self._application))
        webAdminRoot.putChild('extjs', static.File(os.path.dirname(goliat.__file__)+'/static/extjs'))
        webAdminRoot.putChild('goliat', static.File(os.path.dirname(goliat.__file__)+'/static'))
        webAdminRoot.putChild('web', static.File(os.path.dirname(goliat.__file__)+'/web'))
        webAdminRoot.putChild('login', LoginRequest())
        webAdminRoot.putChild('logout', LogoutRequest())
        webAdminRoot.putChild('list', ListServices(self._application))
        webAdminRoot.putChild('start', StartService(self._application))        
        webAdminRoot.putChild('stop', StopService(self._application))
        webAdminRoot.putChild('check_sess', CheckSession())
        webAdminService = internet.TCPServer(cfg['Project']['admin_port'], server.Site(webAdminRoot))
        webAdminService.setName("WebAdmin")
        webAdminService.setServiceParent(self._application)
            

class Service(object):
    _name = 'Service'
    _description = ''
    _port = 0
    _activation = http.datetimeToString()
    _object = None
    _loaded = False 
    
    def __init__(self, name):
        super(Service, self).__init__(self)
        self._name = name.replace('.py', '')
    
    def Load(self):
        if self._loaded: return
        
        _serviceName = "services.{0}".format(self._name)
        _objList = [self._name.capitalize()]        
        _tempModule = __import__(_serviceName, globals(), locals(), _objList) 
        self._object = getattr(_tempModule, _objList[0])() # We need an instance, not a class
        self._description = self._object.getDescription()
        self._port = self._object.getPort()
        self._loaded = True
    
    def isLoaded(self):
        return self._loaded
    
    def getName(self):
        return self._name
    
    def getService(self):
        return self._object
    
    def getPort(self):
        return self._port
    
    def getDescription(self):
        return self._description
    
    def getActivation(self):
        return self._activation 


class ServiceAdminPage(resource.Resource):
    def __init__(self, app):
        self.app = app        
        
    def getChild(self, path, request):
        if path == '' or path == None or path == 'index' or path == 'app':
            return self
        
        return resource.Resource.getChild(self, path, request)

    def render_GET(self, request):
        request.write("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> 
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"> 
    <head> 
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> 
        <meta name="generator" content="Goliat Web Application Framework version 0.1.0" /> 
        <meta name="description" content="Goliat 0.1.0 is a Webframework over Twsited, Orbited and Storm using ExtJS and OpenPhoenixJS as GUI enhancement. Goliat has been developed by Open Phoenix IT SCA." /> 
        <meta name="language" content="{0}" />         
        <link rel="shortcut icon" href="media/favicon.ico" /> 
        <link rel="stylesheet" href="/extjs/resources/css/ext-all.css" type="text/css" /> 
        <link rel="stylesheet" href="/extjs/resources/css/xtheme-gray.css" type="text/css" /> 
        <link rel="stylesheet" href="/goliat/resources/css/crystal.css" type="text/css" /> 
        <script type="text/javascript" characterSet="utf-8" src="/extjs/adapter/ext/ext-base.js"></script> 
        <script type="text/javascript" characterSet="utf-8" src="/extjs/ext-all.js"></script> 
        <script type="text/javascript" characterSet="utf-8" src="/goliat/js/goliat-min.js"></script>
        <!-- <script type="text/javascript" characterSet="utf-8" src="/goliat/js/Loader.js"></script>
        <script type="text/javascript" characterSet="utf-8">
            var Goliat_Loader = new Goliat.Loader();
            Goliat_Loader.loadComponents();
        </script> -->         
        <script type="text/javascript" characterSet="utf-8" src="/web/main.js"></script>
        <script type="text/javascript" characterSet="utf-8" src="/web/ServicesManager.js"></script>        
        <script type="text/javascript" characterSet="utf-8" src="/web/adminservices/ServiceList.js"></script>
        <script type="text/javascript" characterSet="utf-8" src="/web/adminservices/ServiceForm.js"></script>
        <script type="text/javascript" characterSet="utf-8" src="/web/adminservices/LoginWindow.js"></script>
        <title>Goliat {1} :: Web Admin Services</title> 
    </head> 
</html>
        """.format( os.environ['LANG'].split('_')[0], goliat.version.short() ))

        return ''   
                
class StartService(resource.Resource):
    def __init__(self, app):
        self.app = app
        self.serviceName = None
        self.srv = None
        
    def render_POST(self, request):        
        ms = MultiService(self.app)
        config = ConfigManager()
        self.serviceName = request.args.get('name', None)                 
        for srv in IServiceCollection(self.app):
            if not srv.running and srv.name == self.serviceName[0]:
                start = defer.maybeDeferred(srv.startService)
                self.srv = srv
                
        if start != None:
            start.addCallback(self._success, request)
            start.addErrback(self._fail, self.srv, request)
            
            return server.NOT_DONE_YET        
                
        port = ms.getService(self.serviceName[0]).getPort() if ms.getService(self.serviceName[0]) != None else cfg['Project']['app_port']  
        return json.dumps({ 'success' : True, 'name' : self.serviceName[0], 'port' : port })
    
    def _success(self, results, request):        
        ms = MultiService(self.app)
        port = ms.getService(self.serviceName[0]).getPort() if ms.getService(self.serviceName[0]) != None else cfg['Project']['app_port']
        request.write(json.dumps({ 'success' : True, 'name' : self.serviceName[0], 'port' : port }))
        request.finish()
            
    def _fail(self, results, srv, request):
        srv.stopService()        
        ms = MultiService(self.app)  
        port = ms.getService(self.serviceName[0]).getPort() if ms.getService(self.serviceName[0]) != None else cfg['Project']['app_port']
        request.write(json.dumps({ 'success' : False, 'name' : self.serviceName[0], 'port' : port, 'error' : str(results).replace('\n', '<br />') }))
        request.finish()
    

class StopService(resource.Resource):
    def __init__(self, app):
        self.app = app  
        self.serviceName = None
        self.srv = None
        
    def render_POST(self, request):        
        self.serviceName = request.args.get('name', None)        
        for srv in IServiceCollection(self.app):            
            if srv.running and srv.name == self.serviceName[0]:
                self.srv = srv
                stop = defer.maybeDeferred(srv.stopService)
        
        if stop != None:
            stop.addCallback(self._success, request)
            stop.addErrback(self._fail, self.srv, request)
            
            return server.NOT_DONE_YET
        
        return json.dumps({ 'success' : True, 'name' : self.serviceName[0] })
    
    def _success(self, results, request):        
        request.write(json.dumps({ 'success' : True, 'name' : self.serviceName[0] }))
        request.finish()
            
    def _fail(self, results, srv, request):
        srv.stopService()        
        request.write(json.dumps({ 'success' : False, 'name' : self.serviceName[0], 'error' : str(results) }))
        request.finish()

class LoginRequest(resource.Resource):
    def render_POST(self, request):        
        if cfg['Project']['admin'] == request.args['user'][0] and cfg['Project']['password'] == request.args['password'][0]:
            return json.dumps( { 'success': True, 'session': request.getSession().uid } )
                
        return json.dumps({ 'success': False })

class LogoutRequest(resource.Resource):
    def render_POST(self, request):
        request.getSession().expire();
        return json.dumps( { 'success': True } )

class ListServices(resource.Resource):
    def __init__(self,app):
        self.app = app                
    
    def render_GET(self, request):
                
        _sys_services = []
        ms = MultiService(self.app)
        desc = act = ''
        for srv in IServiceCollection(self.app):
            if srv.name == "WebAdmin": continue
            if srv.name == '{0}'.format(cfg['Project']['app_name']+' Application'):
                desc = '''Main web application service.

{0}'''.format(cfg['Project']['app_desc'])
                act = ms.getStartDate()
            
            service = { 'name' : srv.name, 'running' : srv.running, 'description' : desc, 'activation' : act }            
            _sys_services.append(service)        
        
        for srv in _sys_services:
            if srv in ms.getServices().keys():
                srv['description'] = ms.getService(srv).getDescription()
                srv['activation'] = ms.getService(srv).getActivation()
        
        return json.dumps(_sys_services)
        
class CheckSession(resource.Resource):
    def render_GET(self, request):
        return json.dumps({ 'success' : request.getSession().uid == request.args.get('code') })
