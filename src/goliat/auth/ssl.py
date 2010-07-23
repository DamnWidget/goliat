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
# $id goliat/auth/ssl.py created on 17/07/2010 14:56:04 by damnwidget $
'''
Created on 17/07/2010 14:56:04

@license: GPLv2
@copyright: © 2010 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary: SSL/TLS
@version: 0.1
'''
from twisted.internet import ssl

def getContext(key, cert, protocol, verify=False, verify_callback=None,
               verify_loc=None, verify_opts=None):
    """
    Get an SSL context. You should use this method to get a context in Goliat
    rather than creating them directly.
    """
    ctxFactory=ssl.DefaultOpenSSLContextFactory(key, cert, protocol)
    ctx=ctxFactory.getContext()
    if verify:
        if not verify_opts:
            ctx.set_verify(
                ssl.SSL.VERIFY_PEER|
                ssl.SSL.VERIFY_FAIL_IF_NO_PEER_CERT|
                ssl.SSL.VERIFY_CLIENT_ONCE,
                verify_callback)
        else:
            ctxFactory.set_verify(verify_opts, verify_callback)
    if verify_loc and verify:
        if type(verify_loc) is tuple:
            if len(verify_loc) is 1:
                ctx.load_verify_locations(verify_loc[0])
            else:
                ctx.load_verify_locations(verify_loc[0], verify_loc[1])
        else:
            ctx.load_verify_locations(verify_loc)

    ctx.set_options(getattr(ssl.SSL, 'OP_ALL', 0x0000FFFF))

    return ctx

class ContextFactory(object):
    """
    An SSL Context.
    """

    def __init__(self, key, cert, protocol=ssl.SSL.SSLv23_METHOD):
        self.key_file=key
        self.cert_file=cert
        self.protocol=protocol
        self.verify=False

    def getContext(self):
        return getContext(self.key_file, self.cert_file, self.protocol,
            self.verify)

class ContextClientAuthFactory(object):
    """
    An SSL Context with client authentication.    
    """

    def __init__(self, key, cert, loc=None, opts=None,
                 protocol=ssl.SSL.SSLv23_METHOD):
        self.key_file=key
        self.cert_file=cert
        self.protocol=protocol
        self.verify=True
        self.verify_loc=loc
        self.verify_opts=opts

    def getContext(self):
        return getContext(self.key_file, self.cert_file, self.protocol,
            self.verify, self.verify_callback, self.verify_loc,
            self.verify_opts)

    def verify_callback(self, connection, x509, errnum, errdepth, ok):
        if not ok:
            print '{0} is not a valid cert.'.format(x509.get_subject())
            return False
        else:
            return True

