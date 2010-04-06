/*
        
    Goliat : The Twisted and ExtJS Web Application Framwork. 
    Copyright (C) 2010 Open Phoenix IT S.Coop.And.
    Visit us at: http://www.open-phoenix.com
          
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
Ext.ns("${app_name}");
 
var _version = "${app_version}";
        
/**
 * @class ${app_name}.workspace
 * This is the main application class
 * <br />
 * @constructor
 * @singleton
 */
${app_name}.workspace = function() {
    var viewport;
     
    return {
        init: function() {
            this.buildViewPort();
        },
                 
        buildViewPort: function() {
            /*                      
              Add here your own stuff...                      
              For Example:
              tabPanel = new Goliat.TabPanel({
                  region          : 'center',
                  plain           : true,
                  enableTabScroll : true,
                  style           : "padding: 8px 8px 8px 0;",
                  listeners       : this.buildListeners()
              });
                     
              And then add it to the Goliat.LayoutManayer.items below:
              items  : [ tabPanel... ]
                      
              Then define the buildListeners method and add your event callbacks on it...
                      
              End of the example
                      
              REMOVE ME WHEN DONE !
             */
                     
            viewport = new Goliat.LayoutManager({
                layout : '${app_layout}',
                items  : [ ] 
            });
        }    
    }
});

// Main application entry point
Ext.onReady(${app_name}.workspace.init, ${app_name}.workspace)
