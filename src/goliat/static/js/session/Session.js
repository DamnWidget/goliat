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

Ext.ns('Goliat.session');

Goliat.session.Session = Ext.extend(Ext.util.Observable, {
    uid             : null,
    sid             : '',
    name            : 'Anonymous',
    groups          : [],
    creation_date   : '',
    last_login      : '',
    active          : false,
    userProfile     : {},  
    sessionData     : {},
    
    messages        : {
        title       : 'Autentication',
        mask        : 'Please wait...',
        logout      : 'Are you sure do you want to close your session?',
        mask_logout : 'Disconnecting...',
        trans_err   : 'Web transaction failed!.',
        invalid     : 'The returned data is not valid data.',
        401         : 'Username or Password mismatch.',
        409         : 'Already Logged.'
    },
    
    constructor : function(config) {
        Ext.apply(this, config);
        
        this.addEvents({
            /**
             * @event login
             * Fires after session did login
             * @param {Object} this
             */
            login: true,
            
            /**
             * @event logout
             * Fires after session did logout
             * @param {Object} this
             */
            logout: true,
            
            /**
             * @event checked
             * Fires after session did checked
             * @param {Object} this
             */
            checked: true
        });
        
        Goliat.session.Session.superclass.constructor.call(this);
        
        if(this.tpl) {
            if(typeof this.tpl=='string') {
                this.tpl = new Ext.Template(this.tpl);
            }
            this.tpl.compile();
        }
        
        Ext.applyIf(this, {            
            loginWindow : new Goliat.UserLoginWindow({
                title       : this.messages.login,
                scope       : this,
                handler     : this.onLogin,
                url         : '/login'
            }),
            logout      : '/logout'            
        });
    },
    
    onLogin : function() {
        var form = this.loginWindow.get(0);
        if(form.getForm().isValid()) {
            this.loginWindow.el.mask(this.messages.mask, 'x-mask-loading');
            
            form.getForm().submit({
                success : function(form, action) { this.onLoginSuccess(action.result.session); },
                failure : this.onLoginFail,
                scope   : this
            });
        }
    },
    
    onLoginSuccess : function(session) {
        this.loginWindow.el.unmask();
        Ext.apply(this, session);
        this.loginWindow.close();
        this.fireEvent('login', this);
    },
    
    onLoginFail : function(form, response) {
        this.loginWindow.el.unmask();
        eval('var err = '+response.response.responseText);
        if (!this.messages[err.error]) {
            Goliat.Msg.alert(err.message, this);
        } else {
            Goliat.Msg.alert(this.messages[err.error], this);
        }        
    },
    
    onLogout: function() {
        Goliat.Msg.confirm(this.messages.logout, this, function(btn){
            if(btn == 'yes') this.doLogout();
        });
    },
    
    doLogout: function() {
        Ext.getBody().mask(this.messages.mask_logout, 'x-mask-loading');
        
        Ext.Ajax.request({
            method      : 'POST',
            url         : this.logout,
            scope       : this,
            callback    : this.onAfterAjaxReq,
            succCallback: this.onAfterLogout,
            failCallback: function() {
                Goliat.Msg.error('Web transaction failed!', this);
            }
        });
    },
    
    onAfterLogout : function() {
        this.uid = null;
        this.userData = {};
        this.fireEvent('logout', this);
    },
    
    onAfterAjaxReq : function(options, success, result) {
        Ext.getBody().unmask();
        if(success == true) {
            var jsonData;
            try {
                jsonData = Ext.decode(result.responseText);
            } catch(e) {
                Goliat.Msg.error(this.messages.invalid, this);
            }
            options.succCallback.call(options.scope, jsonData, options);
        } else {            
            options.failCallback.call(options.scope, jsonData, options);
        }
    },
    
    check : function() {
        Ext.Ajax.request({
            method      : 'GET',
            url         : this.loginWindow.url,            
            scope       : this,
            callback    : this.onAfterAjaxReq,
            succCallback: function(jsonData, options) {                
                if(jsonData.success) {
                    Ext.apply(this, eval(jsonData.session));                    
                    this.fireEvent('checked', this);                    
                } else {      
                    if (this.failCheckCallback) {
                        if(!this.failCheckCallback(jsonData, options)) {
                            this.loginWindow.show();
                        }
                    }
                    else {
                        this.loginWindow.show();
                    }
                }
            },
            failCallback: function() {
                Goliat.Msg.error(this.messages.trans_err, this);
            }
        });
    },
    
    getData : function() {
        return this.sessionData;
    },
    
    getUserProfile : function() {
        return this.userProfile;
    },
    
    getUid : function() {
        return this.uid;
    },
    
    getSid : function() {
        return this.sid;
    },
    
    getGroups : function() {
        return this.groups;
    },
    
    getCreationDate : function() {
        return this.creation_date;
    },
    
    getLastLogin : function() {
        return this.last_login;
    },
    
    isActive : function() {
        return this.active;
    },
    
    hasGroup : function(group) {
        if(this.groups.indexOf(group) == -1) {
            return false;
        } else {
            return true;
        }
    },
    
    addGroup : function(group) {
        if(this.groups.indexOf(group) == -1) {
            this.groups.push(group);
        }
    },
    
    removeGroup : function(group) {
        if(this.hasGroup(group)) {
            this.groups.splice(this.groups.indexOf(group), 1);
        }
    }   
    
});
