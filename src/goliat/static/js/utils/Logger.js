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

Ext.ns('Goliat.util');

/** 
 * @class Goliat.util.Logger
 * @extends Ext.BoxComponent
 *
 * @author Oscar Campos Ruiz <oscar.campos@open-phoenix.com>
 * @version 0.1
 * @date 2010-03-19 15:23
 *
 */
Goliat.util.Logger = Ext.extend(Ext.BoxComponent, {
    tpl         : new Ext.Template('<li class="x-log-entry x-log-{0:lowercase}-entry">',
        '<div class="x-log-level">',        
        '   <span class="x-log-time">',
        '       {2:date([H:i:s.u])}',
        '   </span>',
        '   <span class="x-log-message">',
        '       {1}',
        '   </span>',
        '</div>',
    '</li>'),
    
    autoEl      : {
        tag: 'ul',
        cls: 'x-logger x-log-show-info'
    },
    
    last        : undefined,   
    
    startMessage: 'Starting Log Console...',
    
    onRender: function() {
        Goliat.util.Logger.superclass.onRender.apply(this, arguments);
        this.contextMenu = new Ext.menu.Menu({
            items: [
                new Ext.menu.CheckItem({
                    id: 'debug',
                    text: 'Debug',
                    checkHandler: Goliat.util.Logger.prototype.onMenuCheck,
                    scope: this
                }),
                new Ext.menu.CheckItem({
                    id: 'info',
                    text: 'Info',
                    checkHandler: Goliat.util.Logger.prototype.onMenuCheck,
                    scope: this,
                    checked: true
                }),
                new Ext.menu.CheckItem({
                    id: 'warning',
                    text: 'Warning',
                    checkHandler: Goliat.util.Logger.prototype.onMenuCheck,
                    scope: this
                }),
                new Ext.menu.CheckItem({
                    id: 'error',
                    text: 'Error',
                    checkHandler: Goliat.util.Logger.prototype.onMenuCheck,
                    scope: this
                })
            ]
        });
        this.el.on('contextmenu', this.onContextMenu, this, {stopEvent: true});
        this.last = this.tpl.insertFirst(this.el, ['debug', this.startMessage, new Date()]);        
    },
    
    onContextMenu: function(e) {
        this.contextMenu.logger = this;
        this.contextMenu.showAt(e.getXY());
    },
    
    onMenuCheck: function(checkItem, state) {
        var logger = checkItem.parentMenu.logger;
        var cls = 'x-log-show-' + checkItem.id;
        if(state) logger.el.addClass(cls);
        else logger.el.removeClass(cls);
    },
    
    debug: function(msg) { 
        this.last = this.tpl.insertAfter(this.last, ['debug', msg, new Date()]);
        this.el.scroll("bottom", this.el.getHeight(), false);         
    },
 
    info: function(msg) { 
        this.last = this.tpl.insertAfter(this.last, ['info', msg, new Date()]);
        this.el.scroll("bottom", this.el.getHeight(), false);
    },
 
    warning: function(msg) {
        this.last = this.tpl.insertAfter(this.last, ['warning', msg, new Date()]);
        this.el.scroll("bottom", this.el.getHeight(), false);
    },
 
    error: function(msg) {
        this.last = this.tpl.insertAfter(this.last, ['error', msg, new Date()]);
        this.el.scroll("bottom", this.el.getHeight(), false);        
    } 
});

Ext.reg('Goliat_logger', Goliat.util.Logger);
