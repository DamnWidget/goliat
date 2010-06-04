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
 * @class Goliat.layout.DisplayLayout
 * @extends Ext.layout.FormLayout
 *  Layout to display information in a displaypanel 
 */
Goliat.layout.DisplayLayout = Ext.extend(Ext.layout.FormLayout, {
    background  : 'none',
    
    onLayout: function(ct, target) {
        Goliat.layout.DisplayLayout.superclass.onLayout.apply(this, arguments);
        
        target.addClass('x-goliat-display-background-' + this.background);        
        if(this.declaration && !this.declEl) {                    
            this.declEl = target.createChild({dom: 'div', html: this.declaration, 'class': 'x-goliat-display-declaration x-goliat-display-background-declaration'});
        }
    },
    
    destroy: function() {
        if(this.declEl) {
            thid.declEl.remove();
        }
        
        Goliat.layout.DisplayLayout.superclass.destroy.call(this);
    }
});

Ext.Container.LAYOUTS['display'] = Goliat.layout.DisplayLayout;
