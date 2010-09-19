/*

  Goliat ExtJS: The Twisted and ExtJS Web Framework
  Copyright (C) 2009-2010  Open Phoenix IT

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

/**
 * @class StompClient
 * @extends Ext.util.Observable
 *
 * @author Oscar Campos Ruiz <oscar.campos@open-phoenix.com>
 * @version 0.1
 */

/**
 * @constructor
 * @param {Object} options  
 */
Goliat.ModelStore = function(options) {
    /**
     * Options
     * @property
     */    
    Ext.apply(this, options);
    
    /**
     * The Model Schema
     * @property
     */
    this.modelSchema = [];   
    
    /**
     * The loaded check
     * @property
     */
    this.loaded = false; 
    
    this.addEvents(
        /**
         * Event onload
         * Fires when the model schema is loaded
         * @param {ModelStoe} The ModelStore object itself                  
         */
        'onload',
        
        /**
         * Event onflush
         * Fires when the model schema is flushed
         * @param {ModelStoe} The ModelStore object itself                  
         */
        'onflush'
    );
    
    // Call the superclass constructor
    Goliat.ModelStore.superclass.constructor.call(this, options);
    
    // Auto Load 
    if(this.autoLoad) {        
        this.load.defer(10, this);        
    }    
};

Ext.extend(Goliat.ModelStore, Ext.util.Observable, {
    messages : { 
        transactionError    : "Error with data transaction.",
        True                : "True",
        False               : "False",
        yes                 : 'Yes',
        no                  : 'No'
    },
    
    load: function() {
        if(!this.url) {
            return { 'success' : false, 'error' : 'No url setted.' }
        }
        Ext.Ajax.request({
            method  : 'GET',
            url     : this.url+'/get_schema_model',            
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
                else {
                    this.modelSchema = response.model;
                    this.loaded = true;
                    this.lookup = {}
                    for(c in this.modelSchema) {
                        if(c == "remove")
                            continue;
                        this.lookup[this.modelSchema[c].name] = this.modelSchema[c];
                    }
                                                        
                    if(!this.store) {                        
                        this.store = this.buildStore();
                        this.store.load();                        
                    }                
                }
            }
        });            
    },
    
    buildStore : function() {
        var proxy = new Ext.data.HttpProxy({
            api : {
                read   : this.url + '/view',
                create : this.url + '/create',
                update : this.url + '/update',
                destroy: this.url + '/destroy'                                
            }
        });
        
        var reader = new Ext.data.JsonReader({
            idProperty          : 'id',
            messageProperty     : 'message',
            successProperty     : 'success'
        }, this.getFields());
        
        var writer = new Ext.data.JsonWriter({
            encode          : true,
            writeAllFields  : false
        });
        
        var store = new Ext.data.Store({
            id        : this.url.replace(/\//g, ''),
            proxy     : proxy,                 
            writer    : writer,
            reader    : reader,
            sortInfo  : { field: 'id', direction: 'ASC' },                            
            autoSave  : true,
            listeners : {
                scope   : this,
                load    : function() {
                    this.fireEvent('onload', this);
                }
            } 
        });
        
        return store;
    },
    
    remove : function(record) {        
        this.store.remove(record);
    },
    
    save : function() {
        this.store.save();
    },
    
    reload: function() {
        this.load();
    },
    
    flush: function() {
        this.modelSchema = null;
        this.fireEvent('onflush', this);
    },
    
    setUrl: function(url) {
        this.url = url;
    },
    
    getModelSchema: function() {
        return this.modelSchema;
    },
    
    getFieldById: function(id) {
        return this.lookup[id];
    },
    
    hasRelation: function(id) {        
        for(var i = 0; i < this.modelSchema.length; i++) {            
            if(this.modelSchema[i].relation !== true)
                continue;
            
            if(!this.modelSchema[i].config.localKey)
                localKey = this.modelSchema[i].config.foreignTable+'_'+this.modelSchema[i].config.foreignKey;
            else
                localKey = this.modelSchema[i].config.localKey;
            
            if(id == localKey)
                return this.modelSchema[i].name;
        }
        
        return false;
    },
    
    getIndexById: function(id) {
        for(c in this.modelSchema) {
            if(c == "remove")
                continue;
            if(this.modelSchema[c].name == id) {
                return c;
            }
        }
        return -1;
    },
    
    moveField: function(oldIndex, newIndex) {        
        var f = this.modelSchema[oldIndex];
        this.modelSchema.splice(oldIndex, 1);
        this.modelSchema.splice(newIndex, 0, f);
    },
    
    getFields: function() {        
        fields = [];        
        for(c in this.modelSchema) {
            if(c == "remove")
                continue;            
            fields.push({ name : this.modelSchema[c].name });
        }        
                
        return fields;
    },
    
    parseFormModel: function() {
        fields_model = Array();        
        for(obj in this.modelSchema) {
            if(!isNaN(obj)) {
                field_data = {};
                if (this.modelSchema[obj].relation === true) {                    
                    continue;
                } else {
                    field_data.fieldLabel = Ext.util.Format.capitalize(this.modelSchema[obj].name.replace(/_/g, ' '));
                    field_data.name = this.modelSchema[obj].name;
                    field_data.anchor = '-10';
                    (this.modelSchema[obj].required) ? field_data.allowBlank = false : field_data.allowBlank = true;
                    (Ext.isDefined(this.modelSchema[obj].config.size)) ? field_data.maxLength = this.modelSchema[obj].config.size : 50;
                    switch(this.parseType(this.modelSchema[obj])) {
                        case 'string':
                            if(Ext.isDefined(this.modelSchema[obj].config.size) && this.modelSchema[obj].config.size <= 100)
                                field_data.xtype = 'textfield';
                            else if(Ext.isDefined(this.modelSchema[obj].config.size) && this.modelSchema[obj].config.size > 100)
                                field_data.xtype = 'textarea';
                            else
                                field_data.xtype = 'textfield';
                            break;
                        case 'number':                       
                            field_data.xtype = 'numberfield';
                            break;     
                        case 'real':
                            field_data.xtype = 'numberfield';
                            field_data.allowDecimals = true;
                            field_data.decimalPrecision = 2;  
                            break;
                        case 'boolean':
                            field_data.xtype = 'radiogroup';
                            field_data.columns = 'auto';
                            field_data.items = [
                                {
                                    inputValue  : '0',
                                    boxLabel    : this.messages['yes']
                                },
                                {
                                    inputValue  : '1',
                                    boxLabel    : this.messages['no']
                                }
                            ];
                            break;                            
                        case 'date':
                        case 'datetime':
                            field_data.xtype = 'datefield';
                            break;
                        case 'time':
                            field_data.xtype = 'timefield';
                            break;                        
                        case 'list':
                            field_data.xtype = 'multiselect';
                            break;
                        default:
                            field_data.xtype = 'textfield';                        
                    }
                    if(this.modelSchema[obj].config.primaryKey)
                        field_data.xtype = 'hidden';    
                    
                    fields_model.push(field_data);   
                }
            }
        }
        
        return fields_model;
    },
    
    parseColumnModel: function() {        
        columns_model = Array();
        for (obj in this.modelSchema) {
            if(!isNaN(obj)) {
                column_data = {};                
                if (this.modelSchema[obj].relation === true)
                    continue;                    
                   
                column_data.header = Ext.util.Format.capitalize(this.modelSchema[obj].name.replace(/_/g, ' '));
                column_data.dataIndex = this.modelSchema[obj].name;
                (this.modelSchema[obj].size) ? column_data.width = this.modelSchema[obj].size : 80;
                column_data.sortable = true; 
                column_data.id = this.modelSchema[obj].name;
                column_data.sqlType = this.parseType(this.modelSchema[obj]);                                
                switch(this.parseType(this.modelSchema[obj])) {
                    case 'string':                        
                        column_data.xtype = 'gridcolumn';                                                
                        break;
                    case 'number':
                        column_data.xtype = 'numbercolumn';
                        column_data.format = '0';                        
                        break;
                    case 'real':
                        column_data.xtype = 'numbercolumn';
                        column_data.format = '0.00';                        
                        break;
                    case 'boolean':
                        if(this.boolImage) { column_data.xtype = 'booleanimagecolumn'; } 
                        else if(this.boolCheck) { column_data.xtype = 'booleancheckcolumn'; } 
                        else { column_data.xtype = 'booleancolumn'; }
                        break;
                    case 'date':
                    case 'time':
                    case 'datetime':
                        column_data.xtype = 'datecolumn';
                        break;
                    case 'list':
                        column_data.xtype = 'arraycolumn';
                        break;
                    default:
                        column_data.xtype = 'gridcolumn';
                        break;
                }                
                if(this.modelSchema[obj].config.primaryKey)
                    column_data.primary = true;
                else
                    column_data.primary = false;                
                columns_model.push(column_data);
            }
        }
                
        return columns_model;    
    },
    
    parseType: function(o) {        
        type = null;
        switch (o.config.type.toLowerCase()) {
            case 'varchar':  
            case 'longvarchar':
            case 'unicode':
            case 'rawstr':
            case 'any':            
                type = 'string';
                break
            case 'integer':            
            case 'smallint':
            case 'longint':
            case 'serial':
            case 'bigserial':
                type = 'number';
                break;
            case 'real':
            case 'float':
            case 'double':
            case 'decimal':            
                type = 'real'
                break;
            case 'bool':
            case 'boolean':
                type = 'boolean';
                break;
            case 'date':
                type = 'date';
                break;
            case 'time':
                type = 'time';
                break;
            case 'timestamp':
                type = 'datetime';
                break;
            case 'timedelta':
                type = 'time';
                break;
            case 'list':
                type = 'array';
                break;
            default:
                type = 'string';
                break;            
        }
        
        return type;
    }
});

