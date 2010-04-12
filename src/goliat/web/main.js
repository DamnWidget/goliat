/*

  Goliat: The Twisted and ExtJS Web Framework
  Copyright (C) 2010  Open Phoenix IT

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  as published by the Free Software Foundation; either version 2
  of the License, or (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

*/

Ext.ns('GoliatServiceAdmin');

var _version = "1.0.0";

/**
 * @class GoliatServiceAdmin.workspace
 * This is the main class for  the Goliat Web Admin Services Application.
 * <br />
 * @constructor
 * @singleton
 */
GoliatServiceAdmin.workspace = function(){
    var viewport, aboutWindow, loginWindow, mainPanel, session;
    
    return {
        init : function() {
            if(!session) {
                if(!loginWindow) {
                    loginWindow = this.buildLoginWindow();
                }
                loginWindow.show();
            } else {
                this.buildViewPort();
            }
        },
        
        buildLoginWindow : function() {
            return new ServiceAdmin.window.UserLoginWindow({
                title       : 'Login to Goliat Services Admin',
                scope       : this,
                handler     : this.onLogin
            });
        },
        
        buildViewPort: function() {
            mainPanel = new Ext.Panel({
                layout      : 'fit',
                border      : false,
                defaults    : { workspace: this },
                items       : [                    
                    {
                        xtype   : 'servicemanager'
                    }
                ],
                tbar        : [         
                    '->',
                    {
                        text        : 'Log Out',
                        iconCls     : 'icon_logout',
                        scope       : this,
                        handler     : this.onLogOut
                    }
                ]
            });
            
            viewport = new Ext.Viewport({
                layout  : 'fit',
                items   : mainPanel
            });
            Ext.getBody().unmask();
        },    
        
        onLogin : function() {            
            var form = loginWindow.get(0);
            if(form.getForm().isValid()) {
                loginWindow.el.mask('Please wait...', 'x-mask-loading');
                
                form.getForm().submit({
                    success : function(form, action) { this.onLoginSuccess(action.result.session); },
                    failure : this.onLoginFail,
                    scope   : this                    
                });
            }            
        },
        
        onLoginSuccess : function(result) {            
            loginWindow.el.unmask();                        
            session = result;
            this.buildViewPort();
            loginWindow.destroy();
            loginWindow = null;
        },
        
        onLoginFail : function() {                        
            loginWindow.el.unmask();
            Goliat.Msg.alert('Login Failed. Please, try again', this);
        },
        
        onLogOut : function() {
            Goliat.Msg.confirm('Are you sure you want to log out?', this, function(btn){
                if(btn == 'yes') this.doLogout();
            });
        },
        
        doLogout : function() {
            Ext.getBody().mask('Logging out...', 'x-mask-loading');
            
            Ext.Ajax.request({
                method      : 'POST',
                url         : '/logout',                
                scope       : this,
                callback    : this.onAfterAjaxReq,
                succCallback: this.onAfterLogout                
            });
        },
        
        onAfterLogout : function() {                        
            this.destroy();
        },
        
        onAfterAjaxReq : function(options, success, result) {
            Ext.getBody().unmask();
            if(success == true) {                
                var jsonData;
                try {
                    jsonData = Ext.decode(result.responseText);
                } catch(e) {
                    Goliat.Msg.error('The returned data is not valid data.', this);
                }
                options.succCallback.call(options.scope, jsonData, options);
            } else {
                Goliat.Msg.error('Web transaction failed!', this);
            }
        },
        
        getSession : function() {
            return session;            
        },
        
        destroy : function() {            
            viewport.destroy();
            session = null;
            viewport  = null;
            mainPanel = null;
            this.init();
        }
    };
}();

Ext.onReady(GoliatServiceAdmin.workspace.init, GoliatServiceAdmin.workspace);
