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
 * @class Goliat.base.GridPanel
 * @extends Ext.grid.GridPanel
 *  A grid panel general implementation.
 * @constructor 
 * @params {Object} config The config Object 
 */
Goliat.base.GridPanel = Ext.extend(Ext.grid.GridPanel, {    
    autoExpandColumn    : 1,
    flex                : 1,    
    border              : false,
    loadMask            : true,    
    trackMouseOver      : false,         
    useModelStore       : false,  
    iconCls             : 'icon_grid',
    viewConfig          : { forceFit : true },    
    enableHdMenu        : false,   
    
    initComponent: function() {
        this.colModel   = this.buildColModel();        
        this.selModel   = this.buildSelModel();        
        this.listeners  = this.buildListeners();      
        
        Goliat.base.GridPanel.superclass.initComponent.call(this, arguments);
        
        if(this.useModelStore)
            this.modelStore = this.buildModelStore();
        else
            this.store = this.buildStore();
    },
    
    buildColModel: function() {        
        return {}
    },
    
    buildSelModel: function() {
        return new Ext.grid.RowSelectionModel({ 
            singleSelect: false, 
            listeners   : { 
                selectionchange: { 
                    scope   : this, 
                    fn      : this.listGrid_onSelectionChange 
                } 
             } 
         });
    },
    
    buildStore: function() {
        return {
            xtype : 'jsonstore'
        }        
    },
    
    buildListeners: function() {
        return {
            scope       : this,
            rowdblclick : this.listGrid_onRowDblClick
        }
    },    
    
    buildModelStore: function() {
        if(!this.useModelStore) {
            this.useModelStore = true;
        }
            
        return new Goliat.ModelStore({
            autoLoad    : true,
            url         : this.modelUrl,
            fieldsOrder : this.columnsOrder,
            listeners   : {
                scope       : this,
                onload      : this.buildColModelStore
            }
        });
    },
    
    buildColModelStore: function() {
        if(!this.modelStore.loaded) {
            this.modelStore.setUrl(this.modelUrl);
            this.modelStore.load();
            this.modelStore.loaded = true;
        }       
        
        this.colModel = new Ext.grid.ColumnModel(this.modelStore.parseColumnModel());        
        this.fixRelations();
        
        if(this.columnsHidden)
            this.hideColumns();
        
        if(this.hidePK)
            this.hidePrimaryKeys();
        
        this.store = this.modelStore.store;                  
    },
    
    hideColumns: function() {
        for (c in this.columnsHidden) {
            if(c === 'remove') continue;
            this.getColumnModel().setHidden(this.getColumnModel().getIndexById(this.columnsHidden[c]), true);
        }
    },
    
    hidePrimaryKeys: function() {
        for(c in this.getColumnsByPK())
            if(c !== 'remove')
                this.getColumnModel().setHidden(this.getColumnModel().getIndexById(this.getColumnsByPK()[c].id), true);
    },
    
    getColumnsByPK: function(){
        return this.getColumnModel().getColumnsBy(function(c) {
            return c.primary === true;
        });
    },
    
    fixRelations: function() {
        for(var i=0; i < this.getColumnModel().getColumnCount(); i++) {
            if(this.getColumnModel().getColumnAt(i).relation === true) {                
                this.relations.push(this.getColumnModel().getColumnAt(i));
                this.getColumnModel().config.splice(i, 1);
            }
        }
    },
    
    load: function(o) {
        if(!this.useModelStore)
            return this.store.load(o);
        
        return this.modelStore.store.load(o);
    },
    
    loadData: function(d) {
        return this.store.loadData(d);
    },
    
    removeAll: function() {
        return this.store.removeAll();
    },
    
    remove: function(r) {
        return this.store.remove(r);
    },
    
    getSelected: function() {
        return this.selModel.getSelections();
    },
    
    getSelectedId: function() {
        var record = this.selModel.getSelected ();
        return record == null ? "" : record.data.id;
    },
    
    listGrid_onRowDblClick: function(grid, rowIndex) {        
        var record = this.store.getAt(rowIndex);        
        new Goliat.EditorWindow({            
            url         : this.modelUrl,
            modelStore  : this.modelStore,
            grid        : this,                     
            record      : record            
        }).show();
    },   
    
    listGrid_onSelectionChange: function() {
        return;
    }
});
