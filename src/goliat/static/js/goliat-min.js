Ext.ns("Goliat");Goliat.TabPanel=Ext.extend(Ext.TabPanel,{messages:{tabAlreadyAdded:"The component panel {0} with type {1} already exists on panel. Skipping...",},initComponent:function(){this.addEvents("log","debug","warn","error");this.itemId="tabPanel";Goliat.TabPanel.superclass.initComponent.call(this)},addPanel:function(a,e){var c=this.items.items;for(var d=0;d<c.length;d++){if(Ext.isString(a)){if(c[d].getXType()===a&&Ext.encode(c[d].data)===Ext.encode(e)){this.activate(c[d]);return}}else{if(c[d].panelType==a.prototype.panelType&&Ext.encode(c[d].data)==Ext.encode(e)){this.activate(c[d]);return}}}if(!e){e={}}if(Ext.isString(a)){Ext.apply(e,{xtype:a});var b=this.add(e);this.activate(b.getItemId())}else{a=new a({data:e});this.add(a);this.activate(a)}}});Ext.reg("Goliat_tabpanel",Goliat.TabPanel);Ext.ns("Goliat.layout");Goliat.layout.ThreeColumnsFLayout=Ext.extend(Object,{type:"goliat-layout",items:[],constructor:function(){this.setup()},setup:function(){sidePanel=new Goliat.SidePanel({itemId:"sidePanel",region:"west",width:208,split:true,minSize:208,maxSize:400,bodyStyle:"background: #ffffff;",items:[],});sidePanel2=new Goliat.SidePanel({itemId:"sidePanel2",region:"east",width:208,split:true,minSize:208,maxSize:400,bodyStyle:"background: #ffffff;",items:[],});centerPanel=new Ext.Panel({layout:"fit",itemId:"centerPanel",region:"center",plain:true,enableTabScroll:true,style:"padding: 8px 0 8px 0;",items:[]});bottomPanel=new Ext.Panel({itemId:"bottomPanel",region:"south",height:100,minSize:100,});this.items=[sidePanel,centerPanel,sidePanel2,bottomPanel]}});Ext.ns("Goliat.layout");Goliat.MainWindowLayout=Ext.extend(Object,{type:"goliat-layout",items:[],constructor:function(){this.setup()},setup:function(){this.items=[]}});Ext.ns("Goliat.layout");Goliat.layout.ThreeColumnsLayout=Ext.extend(Object,{type:"goliat-layout",items:[],constructor:function(){this.setup()},setup:function(){sidePanel=new Goliat.SidePanel({itemId:"sidePanel",region:"west",width:208,split:true,minSize:208,maxSize:400,bodyStyle:"background: #ffffff;",items:[],});sidePanel2=new Goliat.SidePanel({itemId:"sidePanel2",region:"east",width:208,split:true,minSize:208,maxSize:400,bodyStyle:"background: #ffffff;",items:[],});centerPanel=new Ext.Panel({layout:"fit",itemId:"centerPanel",region:"center",plain:true,enableTabScroll:true,style:"padding: 8px 8px 8px 0;",items:[]});this.items=[sidePanel,centerPanel,sidePanel2]}});Ext.ns("Goliat.layout");Goliat.layout.TwoColumnsFLayout=Ext.extend(Object,{type:"goliat-layout",items:[],constructor:function(){this.setup()},setup:function(){sidePanel=new Goliat.SidePanel({itemId:"sidePanel",region:"west",width:208,split:true,minSize:208,maxSize:400,bodyStyle:"background: #ffffff;",items:[],});centerPanel=new Ext.Panel({layout:"fit",itemId:"centerPanel",region:"center",plain:true,enableTabScroll:true,style:"padding: 8px 8px 8px 0;",items:[]});bottomPanel=new Ext.Panel({itemId:"bottomPanel",region:"south",height:100,minSize:100,});this.items=[sidePanel,centerPanel,bottomPanel]}});Ext.ns("Goliat.layout");Goliat.layout.TwoColumnsFhLayout=Ext.extend(Object,{type:"goliat-layout",items:[],constructor:function(){this.setup()},setup:function(){sidePanel=new Goliat.SidePanel({itemId:"sidePanel",region:"west",width:208,split:true,minSize:208,maxSize:400,bodyStyle:"background: #ffffff;",items:[],});centerPanel=new Ext.Panel({layout:"fit",itemId:"centerPanel",region:"center",plain:true,enableTabScroll:true,style:"padding: 8px 8px 8px 0;",items:[]});topPanel=new Ext.Panel({itemId:"topPanel",region:"north",height:60,minSize:60,});bottomPanel=new Ext.Panel({itemId:"bottomPanel",region:"south",height:100,minSize:100,});this.items=[sidePanel,centerPanel,topPanel,bottomPanel]}});Ext.ns("Goliat.layout");Goliat.layout.ThreeColumnsLayout=Ext.extend(Object,{type:"goliat-layout",items:[],constructor:function(){this.setup()},setup:function(){sidePanel=new Goliat.SidePanel({itemId:"sidePanel",region:"west",width:208,split:true,minSize:208,maxSize:400,bodyStyle:"background: #ffffff;",items:[],});sidePanel2=new Goliat.SidePanel({itemId:"sidePanel2",region:"east",width:208,split:true,minSize:208,maxSize:400,bodyStyle:"background: #ffffff;",items:[],});centerPanel=new Ext.Panel({layout:"fit",itemId:"centerPanel",region:"center",plain:true,enableTabScroll:true,style:"padding: 8px 0 8px 0;",items:[]});topPanel=new Ext.Panel({itemId:"topPanel",region:"north",height:60,minSize:60,});this.items=[sidePanel,centerPanel,sidePanel2,topPanel]}});Ext.ns("Goliat.layout");Goliat.layout.TwoColumnsLayout=Ext.extend(Object,{type:"goliat-layout",items:[],constructor:function(){this.setup()},setup:function(){sidePanel=new Goliat.SidePanel({itemId:"sidePanel",region:"west",width:208,split:true,minSize:208,maxSize:400,bodyStyle:"background: #ffffff;",items:[],});centerPanel=new Ext.Panel({layout:"fit",itemId:"centerPanel",region:"center",plain:true,enableTabScroll:true,style:"padding: 8px 8px 8px 0;",items:[]});this.items=[sidePanel,centerPanel]}});Ext.ns("Goliat.layout");Goliat.layout.TwoColumnsHLayout=Ext.extend(Object,{type:"goliat-layout",items:[],constructor:function(){this.setup()},setup:function(){sidePanel=new Goliat.SidePanel({itemId:"sidePanel",region:"west",width:208,split:true,minSize:208,maxSize:400,bodyStyle:"background: #ffffff;",items:[],});centerPanel=new Ext.Panel({layout:"fit",itemId:"centerPanel",region:"center",plain:true,enableTabScroll:true,style:"padding: 8px 8px 8px 0;",items:[]});topPanel=new Ext.Panel({itemId:"topPanel",region:"north",height:60,minSize:60,});this.items=[sidePanel,centerPanel,topPanel]}});Ext.ns("Goliat.layout");Goliat.layout.ThreeColumnsFhLayout=Ext.extend(Object,{type:"goliat-layout",items:[],constructor:function(){this.setup()},setup:function(){sidePanel=new Goliat.SidePanel({itemId:"sidePanel",region:"west",width:208,split:true,minSize:208,maxSize:400,bodyStyle:"background: #ffffff;",items:[],});sidePanel2=new Goliat.SidePanel({itemId:"sidePanel2",region:"east",width:208,split:true,minSize:208,maxSize:400,bodyStyle:"background: #ffffff;",items:[],});centerPanel=new Ext.Panel({layout:"fit",itemId:"centerPanel",region:"center",plain:true,enableTabScroll:true,style:"padding: 8px 0px 8px 0;",items:[]});topPanel=new Ext.Panel({itemId:"topPanel",region:"north",height:60,minSize:60,});bottomPanel=new Ext.Panel({itemId:"bottomPanel",region:"south",height:100,minSize:100,});this.items=[sidePanel,centerPanel,sidePanel2,topPanel,bottomPanel]}});Ext.ns("Goliat.base");Goliat.base.ListPanel=Ext.extend(Ext.Panel,{layout:"fit",initComponent:function(){this.items=this.buildListView();Goliat.base.ListPanel.superclass.initComponent.call(this);this.relayEvents(this.getView(),["click"]);this.relayEvents(this.getStore(),["load"])},buildListView:function(){return{}},buildStore:function(){return{xtype:"jsonstore"}},clearView:function(){this.getStore().removeAll()},clearSelections:function(){return this.getView().clearSelections()},getView:function(){return this.items.items[0]},getStore:function(){return this.getView().store},getSelectedRecords:function(){return this.getView().getSelectedRecords()},getSelected:function(){return this.getSelectedRecords()[0]},refreshView:function(){this.getView().store.reload()},selectById:function(c){var a=this.getView();c=c||false;if(c){var b=a.store.find("id",c);a.select(b)}},loadStoreByParams:function(a){a=a||{};this.getStore().load({params:a})}});Ext.ns("Goliat.base");Goliat.base.FormPanel=Ext.extend(Ext.form.FormPanel,{constructor:function(a){a=a||{};Ext.applyIf(a,{trackResetOnLoad:true});Goliat.base.FormPanel.superclass.constructor.call(this,a)},getValues:function(){return this.getForm().getValues()},isValid:function(){return this.getForm().isValid()},clearForm:function(){var b={};for(var a in this.getValues()){b[a]=""}this.setValues(b);this.data=null},reset:function(){this.getForm().reset()},loadData:function(a){if(a){this.data=a;this.setValues(a)}else{this.clearForm()}},setValues:function(a){return this.getForm().setValues(a||{})}});Goliat.StompClient=function(a){this.options=a;this.socket=Orbited.TCPSocket;this.stomp=undefined;this.verbose=false;this.addEvents("onstompopen","onstompclose","onstomperror","onstomperrorframe","onstompconnectedframe","onstompmessageframe");Goliat.StompClient.superclass.constructor.call(this,a)};Ext.extend(Goliat.StompClient,Ext.util.Observable,{subscribeError:"The stomp service tried to start but there is no channel to subscribe",onopenMessage:"Stomp transport connection was successful.",opcloseMessage:"Stomp connection lost.<br />Reconnection attempt.",onerrorMessage:"Stomp service received an error:<br />",onerrroframeMessage:"Stompservice received an error:<br />",getSocket:function(){return this.socket},getStomp:function(){return this.stomp},stompInit:function(){if(Ext.isEmpty(this.options.channel)){Goliat.Msg.error(this.subscribeError);return}this.stomp=new STOMPClient();this.stomp.onopen=function(){if(this.verbose){Goliat.Msg.alert(onopenMessage)}this.fireEvent("onstompopen",this)};this.stomp.onclose=function(a){Goliat.Msg.error(oncloseMessage);this.stomp.connect();this.fireEvent("onstompclose",this,a)};this.stomp.onerror=function(a){Goliat.Msg.error(onerrorMessage+a);this.fireEvent("onstomperror",this,a)};this.stomp.onerrorframe=function(a){Goliat.Msg.error(onerrorframeMessage+a.body);this.fireEvent("onstomperrorframe",this,a)};this.stomp.onconnectedframe=function(){this.stomp.subscribe(this.options.channel);this.stomp.ready=true;this.fireEvent("onstompconnectedfram",this)};this.stomp.onmessageframe=function(a){this.fireEvent("onstompmessageframe",this,a)}},stompConnect:function(){if(!this.stomp.ready){Goliat.Msg.error("El Cliente Stomp ha intentado conectarse, sin embargo, parece que el servicio no esta bién configurado.");return}if(Ext.isEmpty(this.options.port)){this.options.port=61613}this.stomp.connect(document.domain,this.options.port)},stompDisconnect:function(){this.stomp.disconnect()},stompChannel:function(a){this.options.channel=a},stompPort:function(a){this.options.port=a},changeSubscription:function(a){this.stomp.unsubscribe(this.options.channel);this.options.channel=a;this.stomp.subscribe(a)},onSend:function(a){this.stomp.send(Ext.util.JSON.encode(a),this.options.channel)}});Ext.ns("Goliat.util");Goliat.util.DomHelper=Ext.extend(Object,{constructor:function(a){this.listeners=a.listeners?a.listeners:a},init:function(d){var b,a=this.listeners;for(b in a){if(Ext.isFunction(a[b])){a[b]=this.createHandler(a[b],d)}else{a[b].fn=this.createHandler(a[b].fn,d)}}d.render=d.render.createSequence(function(){var c=d.getEl();if(c){c.on(a)}})},createHandler:function(a,b){return function(c){a.call(this,c,b)}}});Ext.ns("Goliat.util");Goliat.util.Logger=Ext.extend(Ext.BoxComponent,{tpl:new Ext.Template('<li class="x-log-entry x-log-{0:lowercase}-entry">','<div class="x-log-level">','   <span class="x-log-time">',"       {2:date([H:i:s.u])}","   </span>",'   <span class="x-log-message">',"       {1}","   </span>","</div>","</li>"),autoEl:{tag:"ul",cls:"x-logger x-log-show-info"},last:undefined,startMessage:"Starting Log Console...",onRender:function(){Goliat.util.Logger.superclass.onRender.apply(this,arguments);this.contextMenu=new Ext.menu.Menu({items:[new Ext.menu.CheckItem({id:"debug",text:"Debug",checkHandler:Goliat.util.Logger.prototype.onMenuCheck,scope:this}),new Ext.menu.CheckItem({id:"info",text:"Info",checkHandler:Goliat.util.Logger.prototype.onMenuCheck,scope:this,checked:true}),new Ext.menu.CheckItem({id:"warning",text:"Warning",checkHandler:Goliat.util.Logger.prototype.onMenuCheck,scope:this}),new Ext.menu.CheckItem({id:"error",text:"Error",checkHandler:Goliat.util.Logger.prototype.onMenuCheck,scope:this})]});this.el.on("contextmenu",this.onContextMenu,this,{stopEvent:true});this.last=this.tpl.insertFirst(this.el,["debug",this.startMessage,new Date()])},onContextMenu:function(a){this.contextMenu.logger=this;this.contextMenu.showAt(a.getXY())},onMenuCheck:function(b,d){var c=b.parentMenu.logger;var a="x-log-show-"+b.id;if(d){c.el.addClass(a)}else{c.el.removeClass(a)}},debug:function(a){this.last=this.tpl.insertAfter(this.last,["debug",a,new Date()]);this.el.scroll("bottom",this.el.getHeight(),false)},info:function(a){this.last=this.tpl.insertAfter(this.last,["info",a,new Date()]);this.el.scroll("bottom",this.el.getHeight(),false)},warning:function(a){this.last=this.tpl.insertAfter(this.last,["warning",a,new Date()]);this.el.scroll("bottom",this.el.getHeight(),false)},error:function(a){this.last=this.tpl.insertAfter(this.last,["error",a,new Date()]);this.el.scroll("bottom",this.el.getHeight(),false)}});Ext.reg("Goliat_logger",Goliat.util.Logger);Ext.ns("Goliat.util");Goliat.util.Format=function(){return{boolImage:function(a){if(a){return'<img class="icon_on" src="/extjs/resources/images/default/s.gif" title="Running" style="margin: -1px 4px -1px 0; width: 16px; height: 16px; vertical-align: middle;" />'}else{return'<img class="icon_off" src="/extjs/resources/images/default/s.gif" title="Down" style="margin: -1px 4px -1px 0; width: 16px; height: 16px; vertical-align: middle;" />'}}}}();Ext.util.Format.boolImage=Goliat.util.Format.boolImage;Ext.ns("Goliat");Goliat.Loader=function(a){this.options=a;Goliat.Loader.superclass.constructor.call(this,a)};Goliat.Loader=Ext.extend(Ext.util.Observable,{options:{minimal:false,min:false},modules:{"util.Logger":"/goliat/js/utils/Logger","util.Format":"/goliat/js/utils/Format","util.DomHelper":"/goliat/js/utils/DomHelper","base.ListPanel":"/goliat/js/base/ListPanel","base.FormPanel":"/goliat/js/base/FormPanel",LogPanel:"/goliat/js/LogPanel",MessageBox:"/goliat/js/MessageBox",SidePanel:"/goliat/js/SidePanel",TabPanel:"/goliat/js/TabPanel",TwoColumns:"/goliat/js/layout/TwoColumnsLayout",TwoColumnsF:"/goliat/js/layout/TwoColumnsFLayout",TwoColumnsH:"/goliat/js/layout/TwoColumnsHLayout",TwoColumnsFh:"/goliat/js/layout/TwoColumnsFhLayout",ThreeColumns:"/goliat/js/layout/ThreeColumnsLayout",ThreeColumnsF:"/goliat/js/layout/ThreeColumnsFLayout",ThreeColumnsH:"/goliat/js/layout/ThreeColumnsHLayout",ThreeColumnsFh:"/goliat/js/layout/ThreeColumnsFhLayout",MainWindow:"/goliat/js/layout/MainWindowLayout.js",MainWindowMenu:"/goliat/js/layout/MainWindowMenu.js"},loadComponents:function(){for(var a in this.modules){if(this.modules[a]!==false){this.modules[a]=(this.options.minimal||this.options.min)?this.modules[a]+".min.js":this.modules[a]+".js"}}for(var a in this.modules){var c=document.getElementsByTagName("head")[0];var b=document.createElement("script");b.type="text/javascript";b.characterSet="utf-8";b.src=this.modules[a];c.appendChild(b)}}});Ext.ns("Goliat");Goliat.MessageBox=function(){var b={modal:true,resizable:false,closable:false,border:false,constraint:true,constrainHeader:true,stateful:false,plain:true,footer:true,shim:true,bodyStyle:"padding: 8px;",buttonAlign:"center",};informationText="Information";confirmText="Confirmation";errorText="Error";acceptText="Accept";yesText="Yes";noText="No";var a=false;return{show:function(c){Ext.apply(b,c);if(Ext.isWebKit){Ext.apply(b,{width:400})}a=new Ext.Window(b);a.show()},alert:function(d,c,e){this.show({html:d,iconCls:"icon_information",title:informationText,buttons:[new Ext.Button({minWidth:80,iconCls:"icon_accept",text:acceptText,scope:this,handler:function(){a.close()}})]});return this},confirm:function(d,c,e){this.show({html:d,iconCls:"icon_confirm",title:confirmText,buttons:[new Ext.Button({minWidth:80,iconCls:"icon_accept",text:yesText,scope:this,handler:function(){a.close();if(e){e.call(c||window,"yes")}}}),new Ext.Button({minWidth:80,iconCls:"icon_cancel",text:noText,scope:this,handler:function(){a.close();if(e){e.call(c||window,"no")}}})]});return this},error:function(d,c,e){this.show({html:d,iconCls:"icon_error",title:errorText,buttons:[new Ext.Button({minWidth:80,iconCls:"icon_accept",text:acceptText,scope:this,handler:function(){a.close();if(e){e.call(c||window,"ok")}}})]});return this},informationText:"Information",acceptText:"Accept",confirmText:"Confirmation",errorText:"Error",yesText:"Yes",noText:"No"}}();Goliat.Msg=Goliat.MessageBox;Ext.ns("Goliat");Goliat.SidePanel=Ext.extend(Ext.Panel,{messages:{menuAlreadyExists:"The component menu {0} with type {1} already exists at side panel. Skipping..."},style:"padding: 8px;",autoScroll:true,layout:"accordion",layoutConfig:{hideCollapseTool:true,animate:true,fill:false},initComponent:function(){this.addEvents("log","debug","warn","error");Goliat.SidePanel.superclass.initComponent.call(this,arguments)},addMenu:function(d){var b=this.items.items;for(var a=0;a<b.length;a++){if(b[a].menuType==d.menuType){var c=String.format(this.messages.menuAlreadyExists,d.title,d.menuType);this.fireEvent("debug",this,c);return}}this.add(d)},removeMenu:function(c){var b=this.sidePanel.items.items;for(var a=0;a<b.length;a++){if(b[a].menuType==c){this.remove(b[a])}}}});Ext.reg("Goliat_sidepanel",Goliat.SidePanel);Goliat.SidePanelMenu=Ext.extend(Ext.Component,{iconCls:"",title:"",constructor:function(a){a=a||{};this.iconCls=a.iconCls||"no_icon";this.title=a.title||"Undefined";Goliat.SidePanelMenu.superclass.constructor.call(this,a)},initComponent:function(){this.html=String.format('<div class="taskbar_item"><img class="{0}" src="/extjs/resources/images/default/s.gif" />{1}</div>',this.iconCls,this.title);Goliat.SidePanelMenu.superclass.initComponent.call(this)}});Ext.reg("Goliat_sidepanel_menu",Goliat.SidePanelMenu);Ext.ns("Goliat");Goliat.LogPanel=Ext.extend(Ext.Panel,{layout:"fit",enableTabScroll:true,autoScroll:true,margins:"0 0 0 0",bodyStyle:"padding-left: 10px; font-size: 10px;",initComponent:function(){this.logger=new Goliat.util.Logger();this.items=this.logger;Goliat.LogPanel.superclass.initComponent.call(this)},registerLog:function(a,b){switch(a){case"debug":this.logger.debug(b);break;case"warn":this.logger.warning(b);break;case"error":this.logger.error(b);break;default:this.logger.info(b)}}});Ext.reg("Goliat_logpanel",Goliat.LogPanel);