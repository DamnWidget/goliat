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

Ext.ns('Goliat.base');

/**
 * @class Goliat.base.FormPanel
 * @extends Ext.form.FormPanel
 *  An Ext.form.FormPanel general implementation.
 * @constructor 
 * @params {Object} config The config Object
 */
Goliat.base.FormPanel = Ext.extend(Ext.form.FormPanel, {    
    constructor : function(config) {        
        config = config || {};
        Ext.applyIf(config, {
            trackResetOnLoad : true
        });        
        
        Goliat.base.FormPanel.superclass.constructor.call(this, config);
        
        if (this.record) {                        
            this.on({
                scope  : this,
                render : {
                    single : true,
                    fn     : this.loadFormAfterRender
                }
            });
        }
    },
    
    getValues : function() {
        return this.getForm().getValues();
    },
    
    isValid : function() {
        return this.getForm().isValid();
    },
    
    clearForm : function() {
        var newValues = {}
        for(var name in this.getValues()) {
            newValues[name] = '';
        }
        
        this.setValues(newValues);
        this.data = null;
    },
    
    reset : function() {
        this.getForm().reset();
    },
    
    loadData : function(data) {
        if(data) {
            this.data = data;
            this.setValues(data);
        } else {
            this.clearForm();
        }
    },
    
    setValues : function(o) {
        return this.getForm().setValues(o || {});
    },
    
    get: function(o) {
        if(!o.url) {
            return { 'success' : false, 'message' : 'No url setted.' }
        }        
        Ext.Ajax.request({
            method  : 'GET',
            url     : o.url,
            params  : { id : o.id },
            scope   : this,
            callback: function(options, success, request) {
                try {
                    var response = eval("(" + request.responseText + ")"); 
                } catch(e) {}
                if(!response) {
                    Goliat.Msg.error(this.messages.transactionError, this);
                }
                else if(response.success === false) {
                    Goliat.Msg.error(response.error, this);
                }
                else if(o.callback) {
                    o.callback.call(this, response);                    
                }
            }
        });        
    },
    
    loadFormAfterRender: function() {                
        this.get({
            url     : this.url,
            id      : this.record.get('id'),
            callback: function(response) {                             
                this.loadData(response.data);
            }     
        });
    }
}); 
