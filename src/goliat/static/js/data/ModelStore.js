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
    this.options = options || {}
    
    /**
     * The Model Schema
     * @property
     */
    this.modelSchema = [];  
    
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
};

Ext.extend(Goliat.ModelStore, Ext.util.Observable, {
    messages : { 
        transactionError    : "Error with data transaction."
    },
    
    getModelSchema: function() {
        return this.modelSchema;
    },
    
    load: function() {
        if(!this.options.url) {
            return { 'success' : false, 'error' : 'No url setted.' }
        }
        Ext.Ajax.request({
            method  : 'GET',
            url     : this.options.url,
            params  : { 'act' : 'getSchemaModel' },
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
                    this.fireEvent('onload', this);
                }
            }
        });            
    },
    
    reload: function() {
        this.load();
    },
    
    flush: function() {
        this.modelSchema = null;
        this.fireEvent('onflush', this);
    },
    
    setUrl: function(url) {
        this.options.url = url;
    },
    
    getModelSchema: function() {
        return this.modelSchema;
    }
});

