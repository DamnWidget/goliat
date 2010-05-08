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

Ext.ns('Goliat.grid');

Goliat.grid.BooleanImageColumn = Ext.extend(Ext.grid.Column, {
    constructor: function(cfg) {
        Goliat.grid.BooleanImageColumn.superclass.constructor.call(this, cfg);
        this.renderer = Ext.util.Format.boolImage();
    }
});

Goliat.grid.BooleanCheckColumn = Ext.extend(Ext.grid.Column, {
    constructor: function(cfg) {
        Goliat.grid.BooleanImageColumn.superclass.constructor.call(this, cfg);
        this.renderer = Ext.util.Format.boolCheck();
    }
});

Goliat.grid.ArrayColumn = Ext.extend(Ext.grid.Column, {
    constructor: function(cfg) {
        Goliat.grid.ArrayColumn.superclass.constructor.call(this, cfg);
        this.renderer = Ext.util.Format.ellipsis(this.width, true);
    }
});

Ext.apply(Ext.grid.Column.types, {
    booleanimagecolumn: Goliat.grid.BooleanImageColumn,
    booleancheckcolumn: Goliat.grid.BooleanCheckColumn,
    arraycolumn: Goliat.grid.ArrayColumn
});
