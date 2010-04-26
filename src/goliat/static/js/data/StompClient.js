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
 * @class StompClient
 * @extends Ext.Component
 *
 * @author Oscar Campos Ruiz <oscar.campos@open-phoenix.com>
 * @version 0.1
 */

/**
 * @constructor
 * @param {Object} options  
 */
Goliat.StompClient = function(options) {   
    /**
     * Options
     * @property
     */
    this.options = options;
    
    /**
     * The Orbited TCPSocket.
     * @property 
     */
    this.socket = Orbited.TCPSocket;    
    
    /**
     * The Stomp client.
     * @property
     */
     this.stomp = undefined;      
     
     /**
      * Used internally for messaging purposes.
      * @property
      */
     this.verbose = false;
     
     this.addEvents(
        /**
         * @event onstompopen
         * Fires when the Stomp Transport is opened
         * @param {StompClient} this The StompObject iself
         */
        'onstompopen',
        /**
         * @event onstompclose
         * Fires when the Stomp Transport has been closed
         * @param {StompClient} this The StompObject iself
         * @param {String} code The error code 
         */
        'onstompclose',
        /**
         * @event onstomperror
         * Fires when the Stomp Client has errored
         * @param {StompClient} this The StompObject iself
         * @param {String} error The error message
         */
        'onstomperror',
        /**
         * @event onstomperrorframe
         * Fires when there is an error in the received frame
         * @param {StompClient} this The StompObject iself
         * @param {Mixed} frame The frame Object containing the error
         */
        'onstomperrorframe',
        /**
         * @event onstompconnectedframe
         * Fires when the Client is fully set up for sending/receiving
         * @param {StompClient} this The StompObject iself
         */
        'onstompconnectedframe',
        /**
         * @event onstompmessageframe
         * Fires when a message is received
         * @param {StompClient} this The StompObject iself
         * @param {Mixed} frame The frame Object
         */
        'onstompmessageframe'        
     );
     
     // Call the superclass constructor
     Goliat.StompClient.superclass.constructor.call(this, options);
};

Ext.extend(Goliat.StompClient, Ext.util.Observable, {
    /**
     * @cfg {String} subscribeError
     * The text displayed at subscribe error message box.
     */
    subscribeError: 'The stomp service tried to start but there is no channel to subscribe',
    
    /**
     * @cfg {String} onopenMessage
     * The text displayed at stomp connection success message box.
     */
    onopenMessage: 'Stomp transport connection was successful.',
    
    /**
     * @cfg {String} oncloseMessage
     * The text displayed at stomp connection lost message box.
     */
    opcloseMessage: 'Stomp connection lost.<br />Reconnection attempt.',
    
    /**
     * @cfg {String} onerrorMessage
     * The text displayed at stomp error message box.
     */
    onerrorMessage: 'Stomp service received an error:<br />',
    
    /**
     * @cfg {String} onerrorframeMessage
     * The text displayed at stomp frame error message box.
     */
    onerrroframeMessage: 'Stompservice received an error:<br />',    
    
    /**
     * @cfg {String} onconnecterrorMessage
     * The text displayed at stomp connect error message box
     */
    onconnecterrorMessage: 'The Stomp Client tried to connect, but seems like the service is not configured.',
        
    /**
     * Return the Orbited.TCPSocket object being used by this StompClient
     * @return {Orbited.TCPSocket} The Orbited TCPSocket object.
     */
    getSocket: function() {
        return this.socket;
    },
    
    /**
     * Return the Stomp Client Object being used by this StompClient.
     * @return {StompClient} The StompClient object.
     */
    getStomp: function() {
        return this.stomp;
    },    
    
    /**
     * Initialize the Stomp Client. The channel property will be configured with a proper value.
     */
    stompInit: function() {
        if(Ext.isEmpty(this.options.channel)) {
            Goliat.Msg.error(this.subscribeError);            
            return;
        }
        
        // Create the STOMPClient Object
        this.stomp = new STOMPClient();         
    
        // Prepare the Stomp Client
        this.stomp.onopen = function() {
            if(this.verbose) Goliat.Msg.alert(onopenMessage);
            this.fireEvent('onstompopen', this);
        };        
        this.stomp.onclose = function(c) {
            Goliat.Msg.error(oncloseMessage);
            this.stomp.connect();
            this.fireEvent('onstompclose', this, c);
        };   
        this.stomp.onerror = function(error) {
            Goliat.Msg.error(onerrorMessage + error);
            this.fireEvent('onstomperror', this, error); 
        };    
        this.stomp.onerrorframe = function(frame) {
            Goliat.Msg.error(onerrorframeMessage + frame.body);
            this.fireEvent('onstomperrorframe', this, frame); 
        };        
        this.stomp.onconnectedframe = function() { // Run initial connection to STOMP (comet) server
            // Subscribe to channel
            this.stomp.subscribe(this.options.channel)            
            this.stomp.ready = true;
            this.fireEvent('onstompconnectedfram', this)
        };        
        this.stomp.onmessageframe = function(frame) {   // Executed when a message frame is received            
            this.fireEvent('onstompmessageframe', this, frame);
        };
    },
    
    /**
     * Connects to the Stomp (comet) server.
     */
    stompConnect: function() {
        if(!this.stomp.ready) {
            Goliat.Msg.error(this.onconnecterrorMessage);                        
            return;
        }
        
        if(Ext.isEmpty(this.options.port)) this.options.port = 61613;
        this.stomp.connect(document.domain, this.options.port);
    },
    
    /**
     * Disconect from the Stomp (comet) server.
     */
    stompDisconnect: function() {
        this.stomp.disconnect();
    },
    
    /**
     * Sets the Stomp Client channel where subscribe to
     * @param {String} channel
     */
    stompChannel: function(channel) {
        this.options.channel = channel;
    },
    
    /**
     * Sets the Stomp Port where Client will connect to
     * @param {String} port
     */
    stompPort: function(port) {
        this.options.port = port;
    },
    
    /**
     * Change the channel subscription
     * @param {String} channel
     */
    changeSubscription: function(channel) {
        // Unsubscribe the current channel        
        this.stomp.unsubscribe(this.options.channel);
        this.options.channel = channel;
        // Subscribe to the new channel
        this.stomp.subscribe(channel);        
    },
    
    onSend: function(params) {
        this.stomp.send(Ext.util.JSON.encode(params), this.options.channel);
    }
});
 