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

Ext.ns('Goliat');

/**
 * @class Goliat.TabPanel
 * @extends Ext.TabPanel
 *  Create a new TabPanel with methods to add and remove Tabs from it.
 * @constructor 
 * @params {Object} config The config Object
 * @xtype Goliat_tabpanel
 */
Goliat.TabPanel = Ext.extend(Ext.TabPanel, {
    messages        : {        
        tabAlreadyAdded : 'The component panel {0} with type {1} already exists on panel. Skipping...',
    },
    
    initComponent: function() {
        this.addEvents( 'log', 'debug', 'warn', 'error' );
        this.itemId = 'tabPanel';
               
        Goliat.TabPanel.superclass.initComponent.call(this);
    },
    
    addPanel: function(panel, data) {     
        var panels = this.items.items;
        for (var i = 0; i < panels.length; i++) {
            if(Ext.isString(panel)) {
                if(panels[i].getXType() === panel && Ext.encode(panels[i].data) === Ext.encode(data)) {
                    this.activate(panels[i]);                    
                    return;
                }
            } else {            
                if (panels[i].panelType == panel.prototype.panelType && Ext.encode(panels[i].data) == Ext.encode(data)) {
                    this.activate(panels[i]);
                    return;
                }
            }
        }
        
        if(!data) data = {};
        if (Ext.isString(panel)) {
            Ext.apply(data, {
                xtype: panel
            });
            var comp = this.add(data);
            this.activate(comp.getItemId());
        }
        else {
            panel = new panel({
                data: data
            });
            this.add(panel);
            this.activate(panel);
        }        
    }    
});

Ext.reg('Goliat_tabpanel', Goliat.TabPanel);
