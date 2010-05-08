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
 * @class Goliat.util.Format
 * @singleton
 */
Goliat.util.Format = function() {
    return {
        /**
         * Return an image for true or false state.
         * @param {Object} value
         * @param {Object} images
         */
        boolImage: function(value) {
            if(value) {
                return '<img class="icon_on" src="/extjs/resources/images/default/s.gif" title="Running" style="margin: -1px 4px -1px 0; width: 16px; height: 16px; vertical-align: middle;" />';
            } else {
                return '<img class="icon_off" src="/extjs/resources/images/default/s.gif" title="Down" style="margin: -1px 4px -1px 0; width: 16px; height: 16px; vertical-align: middle;" />';
            }
        },
        
        /**
         * Return a checkbox for true or false state.
         * @param {Object} value
         */
        boolCheck: function(value) {
            if(value) {
                return '<input type="checkbox" value="true" checked="checked" />';
            } else {
                return '<input type="checkbox" value="false" />';
            }
        },
        
        /**
         * Return a formated EURO currency for the given amount.
         * @param {Object} value
         */
        eurMoney: function(v) {
            v = (Math.round((v-0)*100))/100;
            v = (v == Math.floor(v)) ? v + ".00" : ((v*10 == Math.floor(v*10)) ? v + "0" : v);
            v = String(v);
            var ps = v.split('.'),
                whole = ps[0],
                sub = ps[1] ? '.'+ ps[1] : '.00',
                r = /(\d+)(\d{3})/;
            while (r.test(whole)) {
                whole = whole.replace(r, '$1' + ',' + '$2');
            }
            v = whole + sub;
            if(v.charAt(0) == '-'){
                return '-' + v.substr(1) + "€";
            }
            return v + "€";
        }        
    };
}();

Ext.apply(Ext.util.Format, Goliat.util.Format);
