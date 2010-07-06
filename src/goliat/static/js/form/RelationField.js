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

Ext.ns('Goliat.form');

Goliat.form.RelationField = Ext.extend(Ext.form.TriggerField, {
    url                 : '',
    triggerClass        : 'x-form-relation-trigger',
    defaultAutoCreate   : {tag: 'input', type: 'text', size: '24', autocomplete: 'off'},
    emptyText           : '',
    loadingText         : 'Loading...',
    relationModel       : 'Object',
    messages            : {
        title   : 'Select a {0}',
        cancel  : 'Cancel',
        select  : 'Select'
    },
    
    initComponent: function() {
        Goliat.form.RelationField.superclass.initComponent.call(this);
        
        this.addEvents(
            /**
             * @event select
             * Fires when a relation is selected using the selector widget
             * @param {Goliat.form.RelationField} this
             * @param {Ext.data.Record} record The data record returned by the underlying store
             * @param {Number} id The id of the selected object in the selector widget 
             */
            'select'
        );
                
        if(this.url == '')
            return;
        
        this.modelStore = new Goliat.ModelStore({
            autoLoad    : true,
            url         : this.url                        
        });
    },
    
    /**
     * @method onTriggerClick
     * @hide
     */
    // private
    // Implements the default empty TriggerField.onTriggerClick function to display the SelectionWindow
    onTriggerClick: function() {
        if(this.readOnly || this.disabled)
            return;
        
        this.sw = new Goliat.SelectionWindow({
            title   : String.format(this.messages.title, this.relationModel),
            iconCls : 'icon_search',            
            items   : new Ext.grid.GridPanel({
                store       : this.modelStore.store,
                colModel    : new Ext.grid.ColumnModel({
                    defaults: {
                        width   : 120,
                        sortable: true
                    },
                    columns: this.modelStore.parseColumnModel()
                }),
                viewConfig  : { forceFit : true },
                sm          : new Ext.grid.RowSelectionModel({singleSelect:true}),
                width       : 600,
                height      : 300
            }),
            buttons : [
                {
                    text    : this.messages.cancel,
                    iconCls : 'icon_cancel',
                    scope   : this,
                    handler : this.cancelButton_onClick
                },
                {
                    text    : this.messages.select,
                    iconCls : 'icon_select',
                    scope   : this,
                    handler : this.selectButton_onClick
                }
            ]            
        });
        this.sw.show();
    },
    
    cancelButton_onClick: function() {
        this.sw.close();
    },
    
    selectButton_onClick: function(m, d) {
        console.debug(m);
        console.debug(d);
    }
    
    
});

Ext.reg('relation', Goliat.form.RelationField);
