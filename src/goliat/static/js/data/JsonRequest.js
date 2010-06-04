/*

  Goliat ExtJS: The Twisted and ExtJS Web Framework
  Copyright (C) 2009-2010  Open Phoenix IT

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

/**
 * @class JsonRequest 
 *
 * @author Oscar Campos Ruiz <oscar.campos@open-phoenix.com>
 * @version 0.1 
 */

Ext.namespace('Goliat.data');

Goliat.data.JsonRequest = function(options, callback) {    
    method = options.method.toUpperCase();
    Ext.Ajax.request({
        method      : method,
        url         : options.url,
        params      : options.data,
        scope       : options.scope,
        callback    : function(options, success, result) {
            Ext.getBody().unmask();
            if(success === true) {
                var jsonData;
                try {
                    jsonData = Ext.decode(result.responseText);                    
                } catch(e) {
                    Goliat.Msg.error('The returned data is not valid data.', this);
                }
                if(callback) {
                    callback.call(options.scope || window, jsonData, options);
                }
            } else {
                Goliat.Msg.error('Web transaction failed!', this);
            }
        }
    });
};
