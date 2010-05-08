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
 * @class Goliat.EditorWindow
 * @extends Ext.Window
 *  A grid panel general implementation.
 * @constructor 
 * @params {Object} config The config Object 
 */
Goliat.EditorWindow = Ext.extend(Ext.Window, {
    layout      : 'fit',
    width       : (Ext.isIE) ? 620 : 590,
    height      : (Ext.isIE) ? 255 : 245,
    modal       : true,    
    resizable   : true,
    draggable   : true,
    center      : true,
    closable    : false,    
    messages    : {
        titlenew        : 'Add new {0}',
        titleedit       : 'Editing : {0}',
        saving          : 'Saving {0}...',
        cancel          : 'Cancel',
        save            : 'Save'
    },
    
    initComponent: function() {        
        Ext.applyIf(this, {
            title   : this.configureTitle(),
            iconCls : (this.record) ? 'icon_edit_edit' : 'icon_edit_add',
            items   : this.buildItems(),
            buttons : this.buildButtons()            
        });
        
        this.addEvents({
            recordsaved: true,
        });
        
        Goliat.EditorWindow.superclass.initComponent.call(this);
    },
    
    buildItems: function() {
        return new Goliat.base.FormPanel({
            url             : this.url,
            bodyStyle       : 'padding: 10px',
            layout          : 'form',
            border          : false,                        
            itemId          : 'recordForm',
            record          : this.record,
            items           : [ this.modelStore.parseFormModel() ],             
            tbar            : null 
        });
    },
    
    buildButtons: function() {
        return [
            {
                text    : this.messages['cancel'],
                iconCls : 'icon_cancel',
                scope   : this,
                handler : this.cancelButton_onClick
            },
            {
                text    : this.messages['save'],
                iconCls : 'icon_save',
                scope   : this,
                handler : this.saveButton_onClick
            }
        ];        
    },
    
    configureTitle: function() {
        if(this.record && this.record instanceof Ext.data.Record) {
            return String.format(
                this.messages.titleedit,
                (this.grid.nameKey) ? this.record.get(this.grid.nameKey) : this.record.get('name')
            );            
        } else {
            return String.format(
                (Ext.isDefined(this.grid) && Ext.isDefined(this.grid.titleName)) ? this.grid.titleName : 'Record'
            );            
        }
    },
    
    cancelButton_onClick: function() {
        this.close();
    }
});
