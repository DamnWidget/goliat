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
 * @class Goliat.base.ListPanel
 * @extends Ext.Panel
 *  An Ext.Panel list based general implementation.
 * @constructor 
 * @params {Object} config The config Object 
 */
Goliat.base.ListPanel = Ext.extend(Ext.Panel, {
    layout  : 'fit',
    
    initComponent : function() {        
        this.items = this.buildListView();
        
        Goliat.base.ListPanel.superclass.initComponent.call(this);
        
        this.relayEvents(this.getView(), ['click']);
        this.relayEvents(this.getStore(), ['load']);
    },
    
    buildListView : function() {
        return {};
    },
    
    buildStore : function() {
        return { xtype : 'jsonstore' };
    },
    
    clearView : function() {
        this.getStore().removeAll();
    },
    
    clearSelections : function() {
        return this.getView().clearSelections();
    },
    
    getView : function() {
        return this.items.items[0];
    },
    
    getStore : function() {
        return this.getView().store;
    },
    
    getSelectedRecords : function() {
        return this.getView().getSelectedRecords();
    },
    
    getSelected : function() {
        return this.getSelectedRecords()[0];    
    },
    
    refreshView : function() {
        this.getView().store.reload();
    },

    selectById : function(id) {
        var view = this.getView();
        id = id || false;
        if (id) {
            var ind = view.store.find('id', id);
            view.select(ind);
        }
    },

    loadStoreByParams : function(params) {
        params = params || {};
        
        this.getStore().load({params:params});
    }    

});
