/*

  Goliat: The Twisted and ExtJS Web Framework
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

Ext.ns('ServiceAdmin.listpanel');

ServiceAdmin.listpanel.ServiceList = Ext.extend(Goliat.base.ListPanel, {
    url : '/list',
    
    buildListView : function() {        
        return {
            xtype           : 'listview',
            singleSelect    : true,
            store           : this.buildStore(),
            style           : 'background-color: #ffffff;',
            columns         : [
                {
                    header      : '<b>Service Name</b>',
                    dataIndex   : 'name'
                },
                {
                    header      : '<b>Running</b>',
                    dataIndex   : 'running',
                    align       : 'center',
                    tpl         : '{running:boolImage}'
                }
            ]
        };
    },
    
    buildStore : function() {
        return {
            xtype       : 'jsonstore',
            autoLoad    : true,
            url         : this.url,
            fields      : [ 'name', {name: 'running', type: 'bool'}, 'description', 'activation' ]            
        };
    } 
});

Ext.reg('servicelist', ServiceAdmin.listpanel.ServiceList);