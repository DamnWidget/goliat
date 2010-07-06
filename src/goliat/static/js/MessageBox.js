/*

  Goliat ExtJS: The Twisted and ExtJS Web Framework
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
 * @class Goliat.MessageBox 
 *  Create a new MessageBox Window.
 * @constructor 
 * @params {Object} config The config Object
 * @xtype Goliat_messagebox
 */
Goliat.MessageBox = function() {
    var opts = {
        modal: true,
        resizable: false,
        closable: false,
        border: false,
        constraint: true,
        constrainHeader: true,
        stateful: false,
        plain: true,        
        footer: true,
        shim: true,
        bodyStyle: "padding: 8px;",
        buttonAlign: "center"
    };    
    
    var dialog = false;
    
    return {
        informationText : 'Information',
        confirmText     : 'Confirmation',
        errorText       : 'Error',
        acceptText      : 'Accept',
        yesText         : 'Yes',
        noText          : 'No',      
        
        show: function(options) {                        
            Ext.apply(opts, options);                        
                    
            if(Ext.isWebKit) Ext.apply(opts, { width: 400 });
                    
            dialog = new Ext.Window(opts);            
            dialog.show();  
             
        },
        
        alert: function(msg, scope, callback) {
            this.show({
                html    : msg,
                iconCls : "icon_information",
                title   : this.informationText,
                buttons : [ new Ext.Button({ minWidth: 80, iconCls : "icon_accept", text    : this.acceptText, scope   : this, handler : function() { dialog.close(); } }) ]
            });
            return this;
        },
        
        confirm: function(msg, scope, callback) {
            this.show({
                html    : msg,
                iconCls : "icon_confirm",
                title   : this.confirmText,
                buttons : [
                    new Ext.Button({
                        minWidth: 80,
                        iconCls: "icon_accept",
                        text: this.yesText,
                        scope: this,
                        handler: function() {
                            dialog.close();
                            if (callback) callback.call(scope || window, "yes");
                        }
                    }),
                    new Ext.Button({
                        minWidth: 80,
                        iconCls: "icon_cancel",
                        text: this.noText,
                        scope: this,
                        handler: function() {
                            dialog.close();
                            if (callback) callback.call(scope || window, "no");
                        }
                    })
                ]      
            });
            return this;
        },
        
        error: function(msg, scope, callback) {
            this.show({
                html    : msg,
                iconCls : "icon_error",
                title   : this.errorText,
                buttons : [ new Ext.Button({ minWidth: 80, iconCls : "icon_accept", text    : this.acceptText, scope   : this,
                    handler : function() {
                        dialog.close();
                        if (callback) callback.call(scope || window, "ok");
                    }
                })]
            });
            return this;
        }       
        
    };    
}();

Goliat.Msg = Goliat.MessageBox;
