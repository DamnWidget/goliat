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

Ext.ns('Goliat.display');

/**
 * @class Goliat.display.DisplayPanel
 * @extends Ext.form.FormPanel
 *  Panel for displaying information on record basis.
 * @xtype Goliat_displaypanel 
 */ 
Goliat.display.DisplayPanel = Ext.extend(Ext.form.FormPanel, {
    cls     : 'x-goliat-display',
    
    layout  : 'display',
    
    itemId  : 'displayPanel',
    
    loadRecord: function(record) {
        return this.getForm().loadRecord(record);
    },
    
    onRender: function() {
        this.supr().onRender.apply(this, arguments);
    }
});

Ext.reg('Goliat_displaypanel', Goliat.display.DisplayPanel);
