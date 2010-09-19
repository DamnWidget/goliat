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
 * @class Goliat.form.RelationField
 * @extends Ext.form.TrifferField
 * Provides a database relation field grid selector with several options as add or remove records.
 * @constructor
 * <p>A relation field selector grid with support for autocomplete, add or remove records and many other features.</p>
 * <p>Example of use:<pre><code>
// create the relation instance
var relation = new Goliat.form.RelationField({
    {@link #url}: '/employeemanager',
    {@link #emptyText}: 'Select a record...',
    {@link #relationModel}: 'Employee',
    {@link #relationManager}: 'EmployeeManager',
    {@link #fieldLabel}: 'Employee',
    {@link #hiddenName}: 'employee_id',
    {@link #valueField}: 'id',
    {@link #displayField}: 'name'
});
 * </code></pre></p>
 * 
 * In the example, we create a new RelationField that will use the url 'http://host.domain/employeemanager' to read
 * data from or write data in. The RelationField will create a new {@link Goliat.ModelStore Store} that will use
 * the url to create his internal CRUD api. For more information about how this work look at {@link Goliat.ModelStore ModelStore} documentation.
 * The {@link #relationManager} is a valid JavaScript class that will manage the creation of new records, this can be the same form used to create
 * the relation objects in their own context. If this option is not setted, the add button will not be available at selector grid.
 * The rest of options are so similar to {@link Ext.form.ComboBox ComboBox} and should work in the same way.
 * @param {Object} config
 * @type relation 
 */
Goliat.form.RelationField = Ext.extend(Ext.form.TriggerField, {
    /**
     * @cfg {String} url
     * The url where the date will be loaded from. Usually a Goliat resource controller.
     */
    url                 : '',
    
    /**
     * @cfg {String} triggerClass
     * An additional CSS class used to style the trigger button.  The trigger will always get the
     * class <tt>'x-form-trigger'</tt> and <tt>triggerClass</tt> will be <b>appended</b> if specified
     * (defaults to <tt>'x-form-search-trigger'</tt> which displays a magnying glass icon).
     */
    triggerClass        : 'x-form-search-trigger',
    
    // private
    defaultAutoCreate   : {tag: 'input', type: 'text', size: '24', autocomplete: 'off'},
    /**
     * @cfg {String} displayField The underlying {@link Ext.data.Field#name data field name} to bind to this
     * RelationField (defaults to undefined ).
     * <p>See also <tt>{@link #valueField}</tt>.</p>     
     */
    /**
     * @cfg {String} valueField The underlying {@link Ext.data.Field#name data value name} to bind to this
     * RelationField (defaults to undefined).
     * <p><b>Note</b>: use of a <tt>valueField</tt> requires the user to make a selection in order for a value to be
     * mapped.  See also <tt>{@link #hiddenName}</tt>, <tt>{@link #hiddenValue}</tt>, and <tt>{@link #displayField}</tt>.</p>
     */
    /**
     * @cfg {String} hiddenName If specified, a hidden form field with this name is dynamically generated to store the
     * field's data value (defaults to the underlying DOM element's name). Required for the relation's value to automatically
     * post during a form submission.  See also {@link #valueField}.
     * <p><b>Note</b>: the hidden field's id will also default to this name if {@link #hiddenId} is not specified.
     * The RelationField {@link Ext.Component#id id} and the <tt>{@link #hiddenId}</tt> <b>should be different</b>, since
     * no two DOM nodes should share the same id.  So, if the ComboBox <tt>{@link Ext.form.Field#name name}</tt> and
     * <tt>hiddenName</tt> are the same, you should specify a unique <tt>{@link #hiddenId}</tt>.</p>
     */
    
    /**
     * @cfg {String} emptyText
     * The string will be displayed when the field is empty
     */
    emptyText           : '',
    
    /**
     * @cfg {String} loadingText The text to display in the dropdown list while data is loading.  Only applies
     * when <tt>{@link #mode} = 'remote'</tt> (defaults to <tt>'Loading...'</tt>)
     */
    loadingText         : 'Loading...',
    
    /**
     * @cfg {String} relationModel The text to display in the window title that represents the relation model
     * we are handling with.
     */
    relationModel       : 'Object',
    
    /**
     * @cfg {Number} queryDelay The length of time in milliseconds to delay between the start of typing and
     * sending the query to filter the selector grid (defaults to <tt>10</tt>)
     */
    queryDelay : 10,
    
    /**
     * @cfg {Number} minChars The minimum number of characters the user must type before autocomplete and
     * {@link #typeAhead} activate (defaults to <tt>0</tt>, does not apply if
     * <tt>{@link Ext.form.TriggerField#editable editable} = false</tt>).
     */
    minChars : 0,    
    
    /**
     * @cfg {Boolean} typeAhead <tt>true</tt> to populate and autoselect the remainder of the text being
     * typed after a configurable delay ({@link #typeAheadDelay}) if it matches a known value (defaults
     * to <tt>false</tt>)
     */
    typeAhead : false,
    
    // private
    messages            : {
        title           : 'Select a {0}',
        cancel          : 'Cancel',
        select          : 'Select',
        add             : 'Add',
        remove          : 'Remove',
        removeConfirm   : 'Are you sure do you want to remove the selected row?' 
    },
    
    // private
    initComponent: function() {
        Goliat.form.RelationField.superclass.initComponent.call(this);
        
        this.addEvents(
             /**
             * @event beforeselect
             * Fires before a list item is selected. Return false to cancel the selection.
             * @param {Goliat.form.RelationField} this This relation field
             * @param {Ext.data.Record} record The data record returned from the underlying store             
             */
            'beforeselect',
            /**
             * @event select
             * Fires when a relation is selected using the selector widget
             * @param {Goliat.form.RelationField} this
             * @param {Ext.data.Record} record The data record returned by the underlying store
             * @param {Number} id The id of the selected object in the selector widget 
             */
            'select',
            /**
             * @event beforequery
             * Fires before all queries are processed. Return false to cancel the query or set the queryEvent's
             * cancel property to true.
             * @param {Object} queryEvent An object that has these properties:<ul>
             * <li><code>combo</code> : Goliat.form.RelationField <div class="sub-desc">This relation field</div></li>
             * <li><code>query</code> : String <div class="sub-desc">The query</div></li>
             * <li><code>forceAll</code> : Boolean <div class="sub-desc">True to force "all" query</div></li>
             * <li><code>cancel</code> : Boolean <div class="sub-desc">Set to true to cancel the query</div></li>
             * </ul>
             */
            'beforequery'
        );
                
        if(this.url == '')
            return;
        
        this.modelStore = new Goliat.ModelStore({
            autoLoad    : true,
            url         : this.url,
            listeners   : {
                scope       : this,
                onload      : function() {
                    this.value = this.emptyText;
                }
            }                            
        });
        
        this.selectedIndex = -1;
    },
    
    // private
    onRender: function(ct, position) {
        if(this.hiddenName && !Ext.isDefined(this.submitValue)){
            this.submitValue = false;
        }
        Goliat.form.RelationField.superclass.onRender.call(this, ct, position);
        if(this.hiddenName) {
            this.hiddenField = this.el.insertSibling({ tag:'input', type:'hidden', name: this.hiddenName, id: (this.hiddenId || this.hiddenName) }, 'before', true);
        }
        
        if(Ext.isGecko){
            this.el.dom.setAttribute('autocomplete', 'off');
        }
    },
    
    // private
    initEvents: function() {
        Goliat.form.RelationField.superclass.initEvents.call(this);
        
        this.keyNav = new Ext.KeyNav(this.el, {
            "up" : function(e) {                
                this.selectPrev();
            },
            
            "down" : function(e) {                
                this.selectNext();
            },
            
            "enter" : function(e) {
                this.onTriggerClick();
            },
            
            "esc" : function(e) {
                if(this.sw) {
                    this.sw.close();
                }
            },
            
            scope : this,            
            forceKeyDown : true,
            defaultEventAction: 'stopEvent'
        });
        
        this.queryDelay = Math.max(this.queryDelay || 10, this.mode == 'local' ? 10 : 250);
        this.dqTask = new Ext.util.DelayedTask(this.initQuery, this);
        if(this.typeAhead){
            this.taTask = new Ext.util.DelayedTask(this.onTypeAhead, this);
        }
        if(!this.enableKeyEvents){
            this.mon(this.el, 'keyup', this.onKeyUp, this);
        }
    },
    
    // private
    onDestroy : function(){
        if (this.dqTask){
            this.dqTask.cancel();
            this.dqTask = null;
        }
        Ext.destroyMembers(this, 'hiddenField');
        Goliat.form.RelationField.superclass.onDestroy.call(this);
    },    
        
    // private
    onTypeAhead : function(){
        if(this.getStore().getCount() > 0){
            var r = this.getStore().getAt(0);
            var newValue = r.data[this.displayField];
            var len = newValue.length;
            var selStart = this.getRawValue().length;
            if(selStart != len){
                this.setRawValue(newValue);
                this.selectText(selStart, newValue.length);
            }
        }
    },
    
    // private
    onSelect : function(record) {        
        if(this.fireEvent('beforeselect', this.getStore(), record) !== false) {
            this.setValue(record.data[this.valueField || this.displayField]);
            this.selectedIndex = this.getStore().indexOf(record);             
            this.sw.close();
            this.fireEvent('select', this, record);
        }
    },
    
    // private
    selectNext : function(){
        var ct = this.getStore().getCount();
        if(ct > 0){
            if(this.selectedIndex == -1) {
                var record = this.getStore().getAt(0);
                this.setValue(record.data[this.valueField || this.displayField]);                
                this.selectedIndex = this.getStore().indexOf(record);                                
            } else if(this.selectedIndex < ct-1) {
                var record = this.getStore().getAt(this.selectedIndex+1);
                this.setValue(record.data[this.valueField || this.displayField]);
                this.selectedIndex = this.getStore().indexOf(record);                                
            }
            
        }
    },

    // private
    selectPrev : function(){
        var ct = this.getStore().getCount();
        if(ct > 0){
            if(this.selectedIndex == -1) {
                var record = this.getStore().getAt(0);
                this.setValue(record.data[this.valueField || this.displayField]);                
                this.selectedIndex = this.getStore().indexOf(record);
            } else if(this.selectedIndex !== 0) {
                var record = this.getStore().getAt(this.selectedIndex-1);
                this.setValue(record.data[this.valueField || this.displayField]);                
                this.selectedIndex = this.getStore().indexOf(record);
            }
        }
    },
    
    // private
    onKeyUp : function(e){
        var k = e.getKey();
        if(this.editable !== false && this.readOnly !== true && (k == e.BACKSPACE || !e.isSpecialKey())){

            this.lastKey = k;
            this.dqTask.delay(this.queryDelay);
        }
        Goliat.form.RelationField.superclass.onKeyUp.call(this, e);
    },
    
    // private
    initQuery : function(){
        this.doQuery(this.getRawValue());
    },
    
    // inherit docs
    getName: function() {
        var hf = this.hiddenField;
        return hf && hf.name ? hf.name : this.hiddenName || Goliat.form.RelationField.superclass.getName.call(this);
    },
    
    /**
     * Execute a query to filter the selector grid.  Fires the {@link #beforequery} event prior to performing the
     * query allowing the query action to be canceled if needed.
     * @param {String} query The query to execute
     * @param {Boolean} forceAll <tt>true</tt> to force the query to execute even if there are currently fewer
     * characters in the field than the minimum specified by the <tt>{@link #minChars}</tt> config option.  It
     * also clears any filter previously saved in the current store (defaults to <tt>false</tt>)
     */
    doQuery : function(q, forceAll){
        q = Ext.isEmpty(q) ? '' : q;
        var qe = {
            query: q,
            forceAll: forceAll,
            combo: this,
            cancel:false
        };
        if(this.fireEvent('beforequery', qe)===false || qe.cancel){
            return false;
        }
        q = qe.query;
        forceAll = qe.forceAll;
        if(forceAll === true || (q.length >= this.minChars)){
            if(this.lastQuery !== q){
                this.lastQuery = q;
                this.selectedIndex = -1;
                if(forceAll){
                    this.getStore().clearFilter();
                } else {                    
                    this.getStore().filter(this.displayField, q);                    
                }                                
            } else {
                this.selectedIndex = -1;
            }
        }
    },
    
    /**
     * Returns the currency selected field value or empty string if not value is set
     * @return {String} value The selected value
     */
    getValue: function() {
        if(this.valueField) {
            return Ext.isDefined(this.value) ? this.value : '';
        } else {
            return Goliat.form.RelationField.superclass.getValue.call(this);
        }
    },
    
    
    /**
     * Sets the specified value into the field.  If the value finds a match, the corresponding record text
     * will be displayed in the field.  If the value does not match the data value of an existing item,
     * and the valueNotFoundText config option is defined, it will be displayed as the default field text.
     * Otherwise the field will be blank (although the value will still be set).
     * @param {String} value The value to match
     * @return {Ext.form.Field} this
     */
    setValue: function(v) {        
        var text = v;
        if(this.valueField) {
            var r = this.findRecord(this.valueField, v);
            if(r) {
                text = r.data[this.displayField];
            } else if(Ext.isDefined(this.valueNotFoundText)) {
                text = this.valueNotFoundText;
            }
        }        
        if(this.hiddenField) {
            this.hiddenField.value = Ext.value(v, '');
        }
        return Goliat.form.RelationField.superclass.setValue.call(this, text);
        this.value = v;
        return this;
    },
    
    // private
    findRecord : function(prop, value){
        var record;
        if(this.getStore().getCount() > 0){
            this.getStore().each(function(r){
                if(r.data[prop] == value){
                    record = r;
                    return false;
                }
            });
        }
        return record;
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
            height      : 300,
            listeners   : {
                scope       : this,
                rowdblclick : this.listGrid_onRowDblClick
            }
        });
        this.grid.relayEvents(this.modelStore.store, ['destroy', 'save', 'update']);
        
        this.sw = new Goliat.SelectionWindow({        
            title   : String.format(this.messages.title, this.relationModel),
            iconCls : 'icon_search',            
            items   : this.grid,
            buttonAlign : 'left',
            buttons : [
                {
                    text    : this.messages.add,
                    iconCls : 'icon_edit_add',
                    hidden  : (this.relationManager) ? false : true,
                    scope   : this,
                    handler : this.addButton_onClick                    
                },                
                {
                    text    : this.messages.remove,
                    iconCls : 'icon_edit_remove',
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
    
    cancelButton_onClick: function() {
        this.sw.close();
    },
    
    selectButton_onClick: function() {
        this.onSelect(this.getGrid().getSelectionModel().getSelected());        
    },
    
    addButton_onClick: function() {
        if(this.relationManager) {
            new this.relationManager().show();            
        }  
    },
    
    removeButton_onClick: function() {
        var record = this.getGrid().getSelectionModel().getSelected();        
        if(!record) {
            return;
        }
        
        Goliat.Msg.confirm(this.messages.removeConfirm, this, function(btn) {
            if(btn == 'yes') {         
                if (this.fireEvent('beforewrite', this.getStore(), 'destroy', record) !== false) {
                    this.getGrid().store.remove(record);
                }
            }
        });
    },
    
    listGrid_onRowDblClick: function(grid, rowIndex) {
        var record = this.getStore().getAt(rowIndex);
        this.onSelect(record);          
    },
    
    getGrid : function() {
        return this.sw.items.items[0];
    },
    
    getStore : function() {
        return  this.modelStore.store;
    }
    
});

Ext.reg('relation', Goliat.form.RelationField);
