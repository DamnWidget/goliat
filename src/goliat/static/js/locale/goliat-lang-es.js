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

if(Goliat.StompClient) {
    Goliat.StompClient.prototype.subscribeError = 'Se ha intentado iniciar el servicio stomp sin definir un canal al que subscribirse.';
    Goliat.StompClient.prototype.onopenMessage = 'La conexión con el Transporte Stomp se ha realizado correctamente.';
    Goliat.StompClient.prototype.oncloseMessage = 'La conexión con el Transporte Stomp se ha perdido.<br />La conexión va a reiniciarse.';
    Goliat.StompClient.prototype.onerrorMessage = 'El servicio Stomp recibió un error:<br />';
    Goliat.StompCLient.prototype.onerrorframeMessage = 'El servicio Stomp recibió un error:<br />';     
}

if(Goliat.util.Logger) {
    Goliat.util.Logger.prototype.startMessage = 'Iniciando Consola de Log...';
}

if(Goliat.MessageBox) {
    Goliat.MessageBox.informationText = 'Información';
    Goliat.MessageBox.confirmText = 'Confirmación';
    Goliat.MessageBox.errorText = 'Error';
    Goliat.MessageBox.acceptText = 'Aceptar';
    Goliat.MessageBox.yesText = 'Si';
    Goliat.MessageBox.noText = 'No';
}

if(Goliat.SidePanel) {
    Goliat.SidePanel.prototype.messages.menuAlreadyExists = 'El menú componente {0} con tipo {1} ya existe en el panel lateral. Saltando...';
}

if(Goliat.TabPanel) {
    Goliat.TabPanel.prototype.messages.tabAlreadyAdded = 'El panel componente {0} con tipo {1} ya existe en el panel. Saltando...';
}
