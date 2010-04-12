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
Ext.ns('ServiceAdmin.form');

ServiceAdmin.form.ServiceForm = Ext.extend(Goliat.base.FormPanel, {   
    
    layout      : {
        type  : 'vbox',
        align : 'stretch'
    },
    
    messages    : {
        selectFromList      : 'Please select a service from the left list',
        alreadyRunning      : 'Service {0} is running already',
        alreadyStopped      : 'Service {0} is stopped already'
    },
    
    initComponent : function() {        
        this.items = [
            this.buildServiceForm()
        ];        
        
        ServiceAdmin.form.ServiceForm.superclass.initComponent.call(this);
        
        this.addEvents({
            /**
             * @event save
             * Fires when the Save Button is clicked.              
             */
            reload  : true,
            
            /**
             * @event stop
             * Fires when the Stop Button is clicked             
             * @param {Object} values from the form
             */
            stop    : true,
            
            /**
             * @event start
             * Fires when the Start Button is clicked             
             * @param {Object} values from the form
             */
            start   : true
        });
    },
    
    buildServiceForm : function() {
        var left = {
            xtype       : 'container',
            layout      : 'form',
            flex        : 1,
            labelWidth  : 60,
            defaultType : 'textfield',
            defaults    : { anchor: '-10' },
            items       : [
                {
                    fieldLabel  : 'Name',
                    name        : 'name',
                    allowBlank  : false,
                    maxLength   : 255,
                    readOnly    : true
                },
                {                    
                    fieldLabel  : 'Activated',
                    name        : 'activation',
                    readOnly    : true
                }
            ]
        };
        
        var right = {
            xtype       : 'container',
            title       : 'Service Description',
            flex        : 1,
            bodyStyle   : 'padding: 1px; margin : 0px;',
            layout      : 'form',
            labelWidth  : 70,
            items       : {
                xtype       : 'textarea',
                fieldLabel  : 'Service Description',
                name        : 'description',
                anchor      : '100% 100%',
                readOnly    : true
            }
        };
        
        return {
            tbar        : this.buildToolbar(),
            layout      : 'hbox',
            height      : 200,
            bodyStyle   : 'padding: 10px;',
            layoutConfig: { align: 'stretch' },
            border      : false,
            items       : [ left, right ]
        };
    },
    
    buildToolbar : function() {
        return [            
            {
                text        : 'Reset',
                iconCls     : 'icon_reload',
                scope       : this,
                handler     : this.resetButton_onClick
            },
            '->',
            {
                text        : 'Start Service',
                iconCls     : 'icon_start',
                scope       : this,
                handler     : this.startButton_onClick
            },            
            {
                text        : 'Stop Service',
                iconCls     : 'icon_stop',
                scope       : this,
                handler     : this.stopButton_onClick
            }
        ]
    },
        
    resetButton_onClick : function() {
        this.fireEvent('reload');
    },
    
    startButton_onClick : function() {
        if (!this.data) {
            Goliat.Msg.error(this.messages.selectFromList, this);
        }
        else if (this.isRunning()) {
            Goliat.Msg.error(String.format(this.messages.alreadyRunning, '<b>' + this.data.name + '</b>'), this);
        } else {
            this.fireEvent('start', this.getValues());           
        }
    },
    
    stopButton_onClick : function() {
        if (!this.data) {
            Goliat.Msg.error(this.messages.selectFromList, this);
        }
        else if (!this.isRunning()) {
            Goliat.Msg.error(String.format(this.messages.alreadyStopped, '<b>' + this.data.name + '</b>'), this);
        } else {
            this.fireEvent('stop', this.getValues());           
        }
    },
    
    isRunning : function() {
        return this.data.running;
    }    
    
});

Ext.reg('serviceform', ServiceAdmin.form.ServiceForm);
