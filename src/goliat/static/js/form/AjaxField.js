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

/**
 * @class Goliat.form.AjaxField
 * @extends Ext.form.RelationField
 * Provides a database ajax field grid selector with several options as add or remove records.
 * @constructor
 * <p>An ajax field selector grid with support for autocomplete, add or remove records and many other features.</p>
 * <p>Example of use:<pre><code>
// create the ajax instance
var relation = new Goliat.form.AjaxField({
    {@link #url}: '/employeemanager',
    {@link #emptyText}: 'Select a record...',        
    {@link #ajaxManager}: 'EmployeeManager',
    {@link #fieldLabel}: 'Employee',
    {@link #hiddenName}: 'employee_id',
    {@link #valueField}: 'id',
    {@link #displayField}: 'name',
    {@link #fields}: ['fullname', 'first']
});
 * </code></pre></p>
 * 
 * In the example, we create a new AjaxField that will use the url 'http://host.domain/employeemanager' to read
 * data from or write data in. The AjaxField will create a new {@link Ext.data.Store} that will use
 * the url to create his internal CRUD api. For more information about how this work look at {@link Ext.data.Store} documentation.
 * The {@link #relationManager} is a valid JavaScript class that will manage the creation of new records, this can be the same form used to create
 * the ajax objects in their own context. If this option is not setted, the add button will not be available at selector grid.
 * The rest of options are so similar to {@link Ext.form.ComboBox ComboBox} and should work in the same way.
 * You can use your own proxy, reader and writer, example:<pre><code>
 // create the ajax instance
var proxy = new Ext.data.HttpProxy({
    api : {
        read    : '/employeemanager/read',
        create  : '/employeemanager/new',
        update  : '/employeemanager/edit',
        destroy : '/employeemanager/delete',
    }
});
var relation = new Goliat.form.AjaxField({    
    {@link #emptyText}: 'Select a record...',        
    {@link #ajaxManager}: 'EmployeeManager',
    {@link #fieldLabel}: 'Employee',
    {@link #hiddenName}: 'employee_id',
    {@link #valueField}: 'id',
    {@link #displayField}: 'name',
    {@link #proxy}: proxy,
    {@link #fields}: ['fullname', 'first']
});
 * </code></pre>
 * 
 * If you use your own reader you will then add your fields propery on it
 * 
 * @param {Object} config
 * @type ajax 
 */
Goliat.form.AjaxField = Ext.extend(Goliat.form.RelationField, {
    /**
     * @cfg {Array/Object} fields
     * Either an array or an object of {@link Ext.data.Field} definition objects 
     */
    /**
     * @cfg {Array} columns An array of {@link Ext.grid.Column columns} to auto create a
     * {@link Ext.grid.ColumnModel}.  
     */
    /**
     * @cfg {Boolean} bool indicating if the remove button will be hidden or not (dedault
     * to true)
     */
    hideRemove : true,
    
    // private
    initComponent : function() {
        this.ajax = true;
        Goliat.form.AjaxField.superclass.initComponent.call(this);
        
        // Create our Ext.data.Store
        this.sc = this.buildStore();   
        
        if(this.ajaxManager) {
            this.ajaxManager = new this.ajaxManager({
                rs          : this.getStore(),
                listeners   : {
                    scope       : this,
                    save        : function(data, store) {                        
                        var rec = new this.grid.store.recordType(data);
                        this.grid.store.insert(0, rec);                        
                    }
                }
            });
        }     
    },
    
    buildStore : function() {
        var proxy = new Ext.data.HttpProxy({
            api : {
                read    : this.url + '/view',
                create  : this.url + '/create',
                update  : this.url + '/update',
                destroy : this.url + '/destroy'
            }
        });
        
        var reader = new Ext.data.JsonReader({
            idProperty      : 'id',
            messageProperty : 'message',
            successProperty : 'success',
            root            : 'data'
        }, this.fields);
        
        var writer = new Ext.data.JsonWriter({
            encode          : true,
            writeAllFields  : false
        });
        
        var store = new Ext.data.Store({
            id          : this.url.replace(/\//g, ''),
            proxy       : this.proxy || proxy,
            writer      : this.writer || writer,
            reader      : this.reader || reader,
            sortInfo    : { field: 'id', direction: 'ASC' },
            autoLoad    : true,
            autoSave    : true                                
        });
        
        return store;
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
        
        this.grid = new Ext.grid.GridPanel({
            store       : this.getStore(),
            colModel    : new Ext.grid.ColumnModel({
                defaults: {
                    width   : 120,
                    sortable: true
                },
                columns: this.columns
            }),
            viewConfig  : { forceFit : true },
            sm          : new Ext.grid.RowSelectionModel({singleSelect:true}),
            width       : 600,
            height      : 300,
            listeners   : {
                scope       : this,
                rowdblclick : this.listGrid_onRowDblClick
            }
        });
        this.grid.relayEvents(this.sc, ['destroy', 'save', 'update']);
        
        this.sw = new Goliat.SelectionWindow({        
            title   : String.format(this.messages.title, this.relationModel),
            iconCls : 'icon_search',            
            items   : this.grid,
            buttonAlign : 'left',
            buttons : [
                {
                    text    : this.messages.add,
                    iconCls : 'icon_edit_add',
                    hidden  : (this.ajaxManager) ? false : true,
                    scope   : this,
                    handler : this.addButton_onClick                    
                },                
                {
                    text    : this.messages.remove,
                    iconCls : 'icon_edit_remove',
                    hidden  : this.hideRemove,
                    scope   : this,
                    handler : this.removeButton_onClick                    
                },            
                '->',
                {
                    text    : this.messages.select,
                    iconCls : 'icon_accept',
                    scope   : this,
                    handler : this.selectButton_onClick
                },
                {
                    text    : this.messages.cancel,
                    iconCls : 'icon_cancel',
                    scope   : this,
                    handler : this.cancelButton_onClick
                }                
            ]              
        });
        this.sw.on('close', function() {
            if (this.selectedIndex < 0) {
                this.focus(true);
            }            
        }, this);
        this.sw.on('show', function() {            
            if(this.selectedIndex > -1) {                
                this.getGrid().getSelectionModel().selectRow(this.selectedIndex);
                this.getGrid().fireEvent('rowclick', this.getGrid(), this.selectedIndex);
                this.getGrid().focus();
            }
        }, this);
        this.sw.show();
    },
    
    addButton_onClick: function() {
        this.ajaxManager.show();
    },
    
    getStore : function() {
        return this.sc;
    }
});

Ext.reg('ajax', Goliat.form.AjaxField);
