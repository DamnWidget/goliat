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

Ext.ns('Goliat');

/**
 * @class Goliat.UserLoginWindow
 * @extends Ext.Window
 * A class to manage application logins
 * @constructor
 */
Goliat.UserLoginWindow = Ext.extend(Ext.Window, {
    messages        : {
        user_login      : 'Login',
        user            : 'User',
        password        : 'Password'
    },
    
    /**
     * @private
     * Configure the component, enforcing defaults
     */
    initComponent : function() {
        Ext.apply(this, {
            width       : 552,
            height      : 572,
            resizable   : false,
            modal       : true,
            closable    : false,
            center      : true,        
            layout      : 'fit',                
            iconCls     : 'icon_login',
            items       : this.buildForm()
        });
        
        if(!this.bodyStyle) {
            Ext.apply(this, { 
                bodyStyle: "background: url(/goliat/resources/media/login.png) no-repeat; padding: 260px 0 0 174px;" 
            })
        }
        
        Ext.applyIf(this, {
            url : '/login'
        });
        
        Goliat.UserLoginWindow.superclass.initComponent.call(this);
    },
    
    buildForm : function() {
        return {
            xtype       : 'form',
            itemId      : 'formPanel',
            defaultType : 'textfield',
            labelWidth  : 72,            
            border      : false,            
            bodyStyle   : 'background: transparent;',                                    
            url         : this.url,
            defaults    : {
                allowBlank      : false,
                labelSeparator  : '',
                width           : 110,
                listeners       : {
                    scope           : this,
                    specialkey      : function(field, e) {
                        if(e.getKey() === e.ENTER && this.handler) {
                            this.handler.call(this.scope);
                        }
                    }
                }
            },
            items       : [
                {
                    fieldLabel  : this.messages.user,
                    name        : 'username'
                },
                {
                    inputType   : 'password',
                    fieldLabel  : this.messages.password,
                    name        : 'password'
                },
                {
                    xtype   : 'button',                    
                    style   : 'margin: 16px 0 0 64px;',
                    iconCls : 'icon_accept',
                    width   : 70,                    
                    text    : this.messages.user_login,
                    handler : this.handler,
                    scope   : this.scope || this
                }
            ]
        };
    }    
});
