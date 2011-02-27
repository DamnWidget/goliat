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
# $id Goliat/src/goliat/template.py created on 04/04/2010 18:33:47 by damnwidget $
'''
Created on 04/04/2010 18:33:47

@license: GPLv2
@copyright: © 2010 - 2011 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary: Goliat Templating System.
@version: 0.2
'''
import os
try:
    from evoque.domain import Domain, get_log
except ImportError:
    raise RuntimeError("Goliat requires evoque module.")

from goliat.utils.apply import Apply
from goliat.utils.borg import Borg


def get_sys_templates_path():
    """Returns the Goliat system templates path"""
    from goliat import __file__ as goliat_file
    return os.path.abspath(os.path.join(os.path.dirname(goliat_file), 'evoque'))

class TemplateManager(Borg):
    """Goliat Template Manager.
    
    Goliat uses evoque as Template Engine.
    TemplateManager inherits from Borg, you can create as many TemplateManager
    objects as you want and them all will share data as long as they refer to
    the same state information.
    
    To create new HTML or XHTML templates you will register a new domain
    do *not* use the system domain because the system domain does not
    escape quotes.     
    """

    _domains=dict()
    _options=dict()

    def __init__(self, options=dict()):
        Borg.__init__(self)
        self._options=Apply(self._options, options)
        # Create the system template if is not present already
        if 'Goliat' not in self._domains:
            self.register_domain(
                'Goliat', get_sys_templates_path(), quoting="str")

    def register_domain(self, name,
                    # Defaults for Domains
                    default_dir,
                    restricted=False, errors=3, log=get_log(),
                    # Defaults for Collections
                    cache_size=0, auto_reload=60, slurpy_directives=True,
                    # Defaults for Collections (and Templates)
                    quoting="xml", input_encoding="utf_8", filters=[]):
        if self.has_domain(name):
            raise ValueError("TemplateManager already has a domain named [%s]" \
                .format(name))
        self._domains[name]=Domain(
            default_dir, restricted, errors, log, cache_size, auto_reload,
            slurpy_directives, quoting, input_encoding, filters)

    def has_domain(self, name):
        return name in self._domains

    def get_domains(self):
        return self._domains

    def get_domain(self, name):
        return self._domains[name] if self.has_domain(name) else None

    def get_sys_domain(self):
        return self._domains['Goliat']

    def __getitem__(self, name):
        return self.get_domain(name)

