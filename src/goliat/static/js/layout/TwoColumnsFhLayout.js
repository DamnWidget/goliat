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

Ext.ns('Goliat.layout');

/**
 * @class Goliat.layout.TwoColumnsFhLayout
 
 * @constructor 
 * @params {Object} config The config Object 
 */
Goliat.layout.TwoColumnsFhLayout = Ext.extend(Object, {
    type: 'goliat-layout',
    items: [],
    
    constructor: function() {
        this.setup();
    },
    
    setup: function() {
        sidePanel = new Goliat.SidePanel({
            itemId          : 'sidePanel',
            region          : 'west',
            width           : 208,
            split           : true,    
            minSize         : 208,
            maxSize         : 400,                
            bodyStyle       : 'background: #ffffff;',
            items           : []
        });
        
        centerPanel = new Ext.Panel({
            layout          : 'fit',
            itemId          : 'centerPanel',
            region          : 'center',
            plain           : true,
            enableTabScroll : true,
            style           : 'padding: 8px 8px 8px 0;',
            items           : []
        });
        
        topPanel = new Ext.Panel({            
            itemId          : 'topPanel',
            region          : 'north',            
            height          : 60,
            minSize         : 60                                                    
        });
        
        bottomPanel = new Ext.Panel({            
            itemId          : 'bottomPanel',
            region          : 'south',            
            height          : 100,
            minSize         : 100                                                    
        });
        
        this.items = [ sidePanel, centerPanel, topPanel, bottomPanel ];
    }
});
