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
 * @class Goliat.Loader 
 *  Loads GoliatJS Components  
 * @constructor 
 * @params {Object} config The config Object 
 */

/**
 * @constructor
 * @param {Object} options The options object
 */
Goliat.Loader = function(options) {   
    this.options = options;
    // Call the superclass constructor
    Goliat.Loader.superclass.constructor.call(this, options); 
};

Goliat.Loader = Ext.extend(Ext.util.Observable, {
    /**
     * The options object defines which GoliatJS Components will be loaded on runtime.     
     * @property
     */
    options : { 'minimal': false, 'min': false }, 
    
    
    /**
     * @property
     */
    modules : {
        'session.Session'   : '/goliat/js/session/Session',
        'ux.Wizard'         : '/goliat/js/ux/Wizard',
        'ux.RowExpander'    : '/goliat/js/ux/RowExpander',
        'ux.SuperBoxSelect' : '/goliat/js/ux/SuperBoxSelect',
        'util.Logger'       : '/goliat/js/utils/Logger',
        'util.Format'       : '/goliat/js/utils/Format',
        'util.DomHelper'    : '/goliat/js/utils/DomHelper',
        'grid.Column'       : '/goliat/js/grid/Column',        
        'base.ListPanel'    : '/goliat/js/base/ListPanel',
        'base.FormPanel'    : '/goliat/js/base/FormPanel',
        'base.GridPanel'    : '/goliat/js/base/GridPanel',
        'form.RelationField': '/goliat/js/form/RelationField',
        'LogPanel'          : '/goliat/js/LogPanel',
        'MessageBox'        : '/goliat/js/MessageBox',
        'SidePanel'         : '/goliat/js/SidePanel',
        'TabPanel'          : '/goliat/js/TabPanel', 
        'base.DetailsPanel' : '/goliat/js/base/DetailsPanel', 
        'AjaxCrossDomain'   : '/goliat/js/AjaxCrossDomain',      
        'StompClient'       : '/goliat/js/StompClient',
        'EditorWindow'      : '/goliat/js/EditorWindow',
        'LoginWindow'       : '/goliat/js/LoginWindow',
        'ModelStore'        : '/goliat/js/data/ModelStore',
        'TwoColumns'        : '/goliat/js/layout/TwoColumnsLayout',
        'TwoColumnsF'       : '/goliat/js/layout/TwoColumnsFLayout',
        'TwoColumnsH'       : '/goliat/js/layout/TwoColumnsHLayout',
        'TwoColumnsFh'      : '/goliat/js/layout/TwoColumnsFhLayout',
        'ThreeColumns'      : '/goliat/js/layout/ThreeColumnsLayout',
        'ThreeColumnsF'     : '/goliat/js/layout/ThreeColumnsFLayout',
        'ThreeColumnsH'     : '/goliat/js/layout/ThreeColumnsHLayout',
        'ThreeColumnsFh'    : '/goliat/js/layout/ThreeColumnsFhLayout',
        'MainWindow'        : '/goliat/js/layout/MainWindowLayout',
        'MainWindowMenu'    : '/goliat/js/layout/MainWindowMenu',
        'DisplayLayout'     : '/goliat/js/layout/DisplayLayout',
        'DisplayPanel'      : '/goliat/js/display/DisplayPanel',
        'DisplayField'      : '/goliat/js/display/DisplayField',
        'TextArea'          : '/goliat/js/display/TextArea',
        'data.JsonRequest'  : '/goliat/js/data/JsonRequest'     
    },
    
    loadComponents: function() {
        // Process with the module load
        for(var i in this.modules) {
            if(this.modules[i] !== false) {                
                this.modules[i] = (this.options['minimal'] || this.options['min']) ? this.modules[i] + '.min.js' : this.modules[i] + '.js';
            }
        }
        
        for(var i in this.modules) {
            var oHead = document.getElementsByTagName('head')[0];
            var oScript = document.createElement('script');
            oScript.type = 'text/javascript';
            oScript.characterSet = 'utf-8';
            oScript.src = this.modules[i];
            oHead.appendChild(oScript);            
        }        
    }    
});
 