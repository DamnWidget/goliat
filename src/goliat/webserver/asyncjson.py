# -*- coding: utf-8 -*-
##
# Goliat: The Twisted and ExtJS Web Framework
# Copyright (C) 2010 - 2011 Open Phoenix IT
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
# $id goliat/webserver/asyncjson.py created on 02/07/2010 23:09:38 by damnwidget $
'''
Created on 02/07/2010 23:09:38

@license: GPLv2
@copyright: © 2010 - 2011 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary:
@version: 0.2
'''
from json import JSONEncoder

from twisted.internet.task import cooperate

class AsyncJSON(object):
    """
    Asynchronous JSON response.
    """

    def __init__(self, value):
        self._value=value

    def begin(self, consumer):
        self._consumer=consumer
        self._iterable=JSONEncoder().iterencode(self._value)
        self._consumer.registerProducer(self, True)
        self._task=cooperate(self._produce())
        defer=self._task.whenDone()
        defer.addBoth(self._unregister)
        return defer

    def pause(self):
        self._task.pause()

    def resume(self):
        self._task.resume()

    def stop(self):
        self._task.stop()

    def _produce(self):
        for chunk in self._iterable:
            self._consumer.write(chunk)
            yield None

    def _unregister(self, passthrough):
        self._consumer.unregisterProducer()
        return passthrough

    def pauseProducing(self):
        self.pause()

    def resumeProducing(self):
        self.resume()

    def stopProducing(self):
        self.stop()
