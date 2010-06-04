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
 * @class Goliat.DetailsPanel
 * @extends Ext.Panel
 *  Create a new DetailsPanel with methods to add and remove Items from it.
 * @constructor 
 * @params {Object} config The config Object
 * @xtype Goliat_detailspanel
 */
Goliat.base.DetailsPanel = Ext.extend(Ext.Panel, {
    /**
     * @cfg {Number} defaultHeight
     * default Heights
     */
    defaultHeight       : 125,    
    
    /**
     * @property record
     * @type Ext.data.Record
     */
    record              : null,
    
    /**
     * @property store
     * @type Ext.data.Store
     */
    store               : null,
    
    /**
     * @property noRecordPanel
     * @type Ext.Panel
     */
    noRecordPanel       : null,
    
    /**
     * @property recordPanel
     * @type Ext.Panel
     */
    recordPanel         : null,
    
    /**
     * @private
     */
    border              : false,
    autoScroll          : true,
    layout              : 'card',
    activeItem          : 0,    
    
    /**
     * Get panel for empty record or not selected yet record
     * 
     * @return {Ext.Panel}
     */
    getNoRecordPanel: function() {
        if(!this.noRecordPanel) {
            this.noRecordPanel = new Ext.Panel(this.defaults);
        }  
        return this.noRecordPanel;
    },
    
    /**
     * Get panel for selected record
     * 
     * @return {Ext.Panel}
     */
    getRecordPanel: function() {
        if(!this.recordPanel) {
            this.recordPanel = new Ext.Panel(this.defaults);            
        }
        return this.recordPanel;
    },
    
    /**
     * Show default template
     * 
     * @param {Mixed} body
     */
    showDefault: function(body) {
        if(this.defaultTpl) {
            this.defaultTpl.overwrite(body);
        }
    },
    
    /**
     * Update template
     * 
     * @param {Ext.data.Record} record
     * @param {Mixed} body
     */
    updateDetails: function(record, body) {
        this.tpl.overwrite(body, record.data);
    },
    
    /**
     * Initialize the component
     */
    initComponent: function() {
        this.defaults = this.defaults || {};
        
        Ext.applyIf(this.defaults, {
            border      : false,
            autoScroll  : true,
            layout      : 'fit'
        });
        
        this.items = [
            this.getNoRecordPanel(),
            this.getRecordPanel()            
        ];
        
        Goliat.base.DetailsPanel.superclass.initComponent.apply(this, arguments);
    },    
    
    /**
     * Update details panel
     * 
     * @param {Ext.grid.RowSelectionModel} sm
     */
    onDetailsUpdate: function(sm) {        
        var count = sm.getCount();
        if (count === 0 || sm.isFilterSelect) {
            this.layout.setActiveItem(this.getNoRecordPanel());
            this.showDefault(this.getNoRecordPanel().body);
            this.record = null;
        } else if (count === 1) {
            this.layout.setActiveItem(this.getRecordPanel());
            this.record = sm.getSelected();
            this.updateDetails(this.record, this.getRecordPanel().body);
        }
    },
    
    /**
     * Get load mask
     * 
     * @return {Ext.LoadMask}
     */
    getLoadMask: function() {
        if (! this.loadMask) {
            this.loadMask = new Ext.LoadMask(this.el);
        }
        
        return this.loadMask;
    }
    
    
});
