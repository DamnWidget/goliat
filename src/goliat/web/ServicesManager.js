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

/**
 * @class GoliatServiceAdmin.ServicesManager
 * @extends Ext.Panel
 * Goliat Services Manager
 * <br />
 * @constructor
 * @param {Object} config The config object
 * @xtype GoliatServiceAdmin_manage_services
 **/
GoliatServiceAdmin.ServicesManager = Ext.extend(Ext.Panel, {
    layout      : 'border',
    border      : false,
    
    messages    : {        
        startService        : 'Starting {0}...',
        stopService         : 'Stopping {0}...',
        succServiceStart    : '{0} service has been started at port {1}',
        failServiceStart    : '{0} service failed to start on port {1}, the service returned this message:<br /><br />{2}',
        succServiceStop     : '{0} service has been stopped',
        failServiceStop     : '{0} service failed to stop, the service returned this message:<br /><br />{1}'
    },        
    
    initComponent   : function() {        
        this.items = [
            this.buildServicesList(),
            this.buildServicesForm()
        ];        
        
        GoliatServiceAdmin.ServicesManager.superclass.initComponent.call(this);        
    },
    
    buildServicesList : function() {
        return {
            xtype       : 'servicelist',
            itemId      : 'serviceList',                        
            flex        : 1,
            split       : true,            
            resizable   : true,            
            region      : 'west',            
            width       : 208,            
            minSize     : 208,
            maxSize     : 400,
            border      : true,
            margins     : '0 0 0 0',
            bodyStyle   : "font-size: 10px;",
            style       : "padding: 8px;",
            autoScroll  : true,
            listeners   : {
                scope : this,
                click : this.serviceList_onClick
            }            
        };
    },
    
    buildServicesForm : function() {        
        return {
            xtype       : 'serviceform',
            itemId      : 'serviceForm',
            region      : 'center',
            border      : true,
            margins     : '0 0 0 0',            
            style       : 'padding: 8px 8px 8px 0;',            
            listeners   : {
                scope       : this,
                reload      : this.onReload,      
                start       : this.onStartService,
                stop        : this.onStopService
            }            
        }
    },
    
    serviceList_onClick : function() {
        var selectedService = this.getComponent('serviceList').getSelected();  
        this.getComponent('serviceForm').loadData(selectedService.data);      
    },    
    
    clearFormPanel : function() {
        this.getComponent('serviceList').clearSelections();
        this.getComponent('serviceForm').clearForm();
    },
    
    cleanSlate : function() {
        this.getComponent('serviceList').refreshView();
    },
    
    onReload : function() {
        Ext.getBody().mask(this.messages.reload, 'x-mask-loading');
        this.refresh();
    },
    
    onStartService : function(data) {
        Ext.getBody().mask(String.format(this.messages.startService, data.name), 'x-mask-loading');
        
        this.getComponent('serviceForm').getForm().submit({
            url     : '/start',
            scope   : this,
            success : this.startService_onSuccess,
            failure : this.startService_onFail
        });                
    },
    
    onStopService : function(data) {
        Ext.getBody().mask(String.format(this.messages.stopService, data.name), 'x-mask-loading');
        
        this.getComponent('serviceForm').getForm().submit({
            url     : '/stop',
            scope   : this,
            success : this.stopService_onSuccess,
            failure : this.stopService_onFail
        });
    },     
    
    startService_onSuccess : function(form, action) {        
        Ext.getBody().unmask();
        Goliat.Msg.alert(String.format(this.messages.succServiceStart, action.result.name, action.result.port), this);
        this.refresh();
    },
    
    startService_onFail : function(form, action) {
        Ext.getBody().unmask();
        Goliat.Msg.alert(String.format(this.messages.failServiceStart, action.result.name, action.result.port, action.result.error), this);
    },
    
    stopService_onSuccess : function(form, action) {        
        Ext.getBody().unmask();
        Goliat.Msg.alert(String.format(this.messages.succServiceStop, action.result.name), this);
        this.refresh();
    },
    
    stopService_onFail : function(form, action) {
        Ext.getBody().unmask();
        Goliat.Msg.alert(String.format(this.messages.failServiceStop, action.result.name, action.result.error), this);
    },
    
    refresh : function() {
        this.clearFormPanel();
        this.cleanSlate();
        Ext.getBody().unmask();
    }    
    
});

Ext.reg('servicemanager', GoliatServiceAdmin.ServicesManager);
