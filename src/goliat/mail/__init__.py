# -*- coding: utf-8 -*-
##
# Goliat: The Twisted and ExtJS Web Framework
# Copyright (C) 2010 Open Phoenix IT
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
##
# $id goliat/mail/__init__.py created on 14/10/2010 15:31:24 by damnwidget $
'''
Created on 14/10/2010 15:31:24

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary: Email sending with or without authentication
@version: 0.1
'''

from OpenSSL.SSL import SSLv3_METHOD
from twisted.mail.smtp import ESMTPSenderFactory, sendmail
from twisted.internet.ssl import ClientContextFactory
from twisted.internet.defer import Deferred
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email import Encoders
import sys
import mimetypes
import os

class Email(Object):
    """
    Class used to send emails without authentication
    """

    _smtphost='localhost'
    _port=25

    def __init__(self, fromaddr, toaddrs, subject, body, filenames=[]):
        self._from=fromaddr
        self._to=toaddrs
        self._message=MIMEMultipart('alternative')
        self._message['From']=fromaddr
        self._message['To']=', '.join(toaddrs)
        self._message['Subject']=subject
        textPart=None
        htmlPart=None
        if dict is type(body):
            textPart=MIMEText(body['text'], 'plain')
            htmlPart=MIMEText(body['html'], 'html')
        else:
            textPart=MIMEText(body, 'plain')

        self._message.attach(textPart)
        if htmlPart:
            self._message.attach(htmlPart)

        for filename in filenames:
            # Guess the mimetype
            mimetype=mimetypes.guess_type(filename)[0]
            if not mimetype:
                mimetype='application/octet-stream'
            maintype, subtype=mimetype.split('/')
            attachment=MIMEBase(maintype, subtype)
            attachment.set_payload(file(filename).read())
            # base64 encode for safety
            Encoders.encode_base64(attachment)
            # Include file name information
            attachment.add_header('Content-Disposition', 'attachment',
                filename=os.path.split(filename)[1])

            self._message.attach(attachment)

    def set_host(self, host):
        try:
            self._smtphost, self._port=host.split(':')
        except ValueError:
            self._smtphost=host

    def send(self):
        messageData=self._message.as_string()
        sending=sendmail(self._smtphost, self._from, self._to, messageData,
            self._port)
        return sending

class AuthEmail(Email):
    """
    Class used to send emails with authentication
    """

    def __init__(self, user, passwd, fromaddr, to, subject, body, files=[]):
        self._username=user
        self._password=passwd
        super(AuthEmail, self).__init__(fromaddr, to, subject, body, files)


    def send(self):
        ctx=ClientContextFactory()
        ctx.method=SSLv3_METHOD

        result=Deferred()

        sender=ESMTPSenderFactory(
            user, passwd, fromaddr, to, self._message, result,
            contextFacory=ctx)

        from twisted.internet import epollreactor
        epollreactor.connectTCP(self._smtphost, self._port, sender)

        return result
