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

Ext.ns('Goliat');

/**
 * @class Goliat.Many2onePanel
 * @extends Ext.grid.GridPanel
 *  Create a new Many2one Goliat panel..
 * @constructor 
 * @params {Object} config The config Object
 * @xtype Goliat_Many2onepanel
 */
Goliat.Many2onePanel = Ext.extend(Ext.grid.GridPanel, {
    messages : {},
    
    modelStore : {
        xtype       : 'modelstore',
        url         : '',
        autoLoad    : false,
        fields      : [ 'name', {name: 'fields', type: 'Object'} ]        
    },
    
    initComponent: function() {
        this.addEvents( 'log', 'debug', 'warn', 'error' );
        this.itemId = 'many2onePanel';
        
        Goliat.Many2onePanel.superclass.initComponent.call(this);
        // Loads the model
        this.loadModel();
    },
    
    loadModel: function() {
        
    }
});
