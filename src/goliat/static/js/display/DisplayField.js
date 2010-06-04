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
 * @class Goliat.display.DisplayField
 * @extends Ext.form.DisplayField
 *  Field for displaying information on record basis.
 * @xtype Goliat_displayfield 
 */ 
Goliat.display.DisplayField = Ext.extend(Ext.form.DisplayField, {
    htmlEncode  : true,
    nl2br       : false,
    
    renderer: function(v) {
        return v;
    },
    
    setRawValue: function(value) {
        var v = this.renderer(value);
        
        if(this.htmlEncode) {
            v = Ext.util.Format.htmlEncode(v);
        }
        
        if(this.nl2br) {
            v = Ext.util.Format.nl2br(v);
        }       
        
        return this.rendered ? (this.el.dom.innerHTML = (Ext.isEmpty(v) ? '' : v)) : (this.value = v);
    }
});

Ext.reg('Goliat_displayfield', Goliat.display.DisplayField);
