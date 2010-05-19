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
# $id goliat/auth/login.py created on 18/05/2010 19:12:32 by damnwidget $
'''
Created on 18/05/2010 19:12:32

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary:
@version: 0.1
'''
from twisted.web import static, resource
import os
import re

from goliat._version import version
from goliat.http import headers
from goliat.template import TemplateManager
import goliat

class Login(resource.Resource):

    def __init__(self, config):
        self.config=config

    def getChild(self, path, request):
        """
        Disable url dispatching.
        """
        return self

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
        <meta name="language" content="EN" />
        <title>Goliat :: Web Admin Services</title> 
        <style type="text/css">
            body {
                color: black;
                font-size: 11px;
            }
            #login {            
                width: 230px;
                margin: 200px auto;
            }
            #login p{
                text-align: center;
                font-size: 18px;
                font-weight: bold;
            }
            #login-form {
                padding: 20px;
                background-color: #ffc9a5;
                border: solid 2px #000000;
                -moz-border-radius: 10px;  
                -webkit-border-radius: 10px;
                border-radius: 10px;
            }
        </style>
        <script type="text/javascript">
            function ajaxRequest() {
                if(window.XMLHttpRequest) {
                    xhr=new XMLHttpRequest();
                } else {
                    xhr=new ActiveXObject("Microsoft.XMLHTTP");
                }
            
                xhr.onreadystatechange=function() {
                    if(xhr.readyState==4 && xhr.status==200) {                        
                        document.location.href='/';                        
                    }
                }
                
                form = document.getElementById('login-form');
                uname = form.username.value;
                upwd = form.password.value;
                xhr.open('GET', '/?username='+uname+'&password='+upwd, true);
                xhr.send();
            }            
        </script>
    </head> 
    <body>
        <div id="login">
            <p>Authorization Request</p>
            <form id="login-form" action="javascript:ajaxRequest();" method="GET">
                Username:
                <input type="text" name="username" />
                Password:
                <input type="password" name="password" /><br /><br />
                <input type="submit" value="Login" />
                <input type="reset" />
            </form>
        </div>
    </body>
</html>
        """)

        return ''
