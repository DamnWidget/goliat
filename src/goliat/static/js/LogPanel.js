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
 * @class Goliat.LogPanel
 * @extends Ext.Panel
 *  Create a new LogPanel that registerer every application log, debug, warning or error message.
 * @constructor 
 * @params {Object} config The config Object
 * @xtype Goliat_logpanel
 */
Goliat.LogPanel = Ext.extend(Ext.Panel, {
    layout          : 'fit',
    enableTabScroll : true,
    autoScroll      : true,
    margins         : '0 0 0 0',
    bodyStyle       : "padding-left: 10px; font-size: 10px;",
    
    initComponent: function() {
        // Create the logger object
        this.logger = new Goliat.util.Logger();
        
        // Add the logger to the panel.        
        this.items = this.logger;
         
        
        // Call the superclass initComponent constructor.
        Goliat.LogPanel.superclass.initComponent.call(this);
    },
    
    registerLog: function(severity, msg) {
        switch(severity) {
            case 'debug':
                this.logger.debug(msg);
                break;
            case 'warn':
                this.logger.warning(msg);
                break;
            case 'error':
                this.logger.error(msg);
                break;
            default:
                this.logger.info(msg);
        }
    }
});

Ext.reg('Goliat_logpanel', Goliat.LogPanel);
