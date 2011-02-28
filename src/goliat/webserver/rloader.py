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
# $id goliat/webserver/resourcesloader.py created on 02/04/2010 13:28:44 by damnwidget
from twisted.internet.inotify import humanReadableMask
from hgext.convert.cvsps import len
'''
Created on 02/04/2010 13:28:44

@license: GPLv2
@copyright: © 2010 - 2011 Open Phoenix IT SCA
@organization: Open Phoenix IT S.Coop.And
@author: Oscar Campos
@contact: oscar.campos@open-phoenix.com
@summary: Web Server resources loader module
@version: 0.2
'''
import os
import re
from datetime import datetime
from twisted.python import filepath
from twisted.web import static
from goliat.module import Module
from twisted.internet import inotify

import goliat


class ResourcesLoader(object):
    """ResourcesLoader Object."""
    _root=None
    _modules=list()
    _modules_loaded=False
    _scripts=[]
    _styles=[]
    _app_path='application'
    _script_path='view'
    _options=dict()

    def __init__(self, root, options=dict()):
        self._root=root
        self._options=options
        self._load_scripts()
        self._load_styles()
        self._notifier=inotify.INotify()
        self._notifier.startReading()
        self._notifier.watch(
            filepath.FilePath("application/controller"),
            callbacks=[self._notify]
        )
        self._module_manager=None

    def setup(self, module_manager):
        """Setup the loader and load the Goliat Application files"""
        self._module_manager=module_manager
        # ===========================
        # Resources
        # ===========================

        # Orbited related
        if self._options['orbited']:
            import orbited # For get the __file__            
            # Add static URL to Goliat Page Hierarchy so we can add
            # Stomp JS files on Application         
            self._root.putChild('static',
                    static.File(os.path.dirname(orbited.__file__)+'/static'))

        # ExtJS related
        self._root.putChild('extjs',
                static.File(os.path.dirname(goliat.__file__)+'/static/extjs'))

        # Goliat related
        self._root.putChild('goliat',
                static.File(os.path.dirname(goliat.__file__)+'/static'))

        # Goliat application related
        self._root.putChild('ui',
                static.File('{0}/{1}'.format(
                    self._app_path, self._script_path)))
        self._root.putChild('js', static.File('web/js'))
        self._root.putChild('media', static.File('web/media'))
        self._root.putChild('css', static.File('web/css'))

        # User paths related
        for key, value in self._options['respath'].iteritems():
            if filepath.FilePath(value).exists():
                self._root.putChild(key, static.File(value))

        # ===========================
        # CSS Styles
        # ===========================

        # ExtJS
        self._root.add_style(
            '<link rel="stylesheet" href="/extjs/resources/css/ext-all.css" ' \
            'type="text/css" />')
        self._root.add_style(
            '<link rel="stylesheet" href="/extjs/resources/css/{0}.css" ' \
            'type="text/css" />'.format(self._options['extjsTheme']))

        # Goliat
        self._root.add_style(
            '<link rel="stylesheet" href="/goliat/resources/css/{0}.css" ' \
            'type="text/css" />'.format(self._options['goliatTheme']))

        # Application UI
        for ui_style in self._styles:
            self._root.add_style(
                '<link rel="stylesheet" href="css/{0}" ' \
                'type="text/css" />'.format(ui_style))

        # ===========================
        # JavaScript
        # ===========================

        # Orbited
        if self._options['orbited']:
            self._root.add_script(
                '<script type="text/javascript" characterSet="utf-8" ' \
                'src="/static/Orbited.js"></script>')
            self._root.add_script(
                '<script type="text/javascript" characterSet="utf-8" ' \
                'src="/static/protocols/stomp/stomp.js"></script>')

        # ExtJS
        if self._options['debug']:
            self._root.add_script(
                '<script type="text/javascript" characterSet="utf-8" ' \
                'src="/extjs/adapter/ext/ext-base-debug.js"></script>')
            self._root.add_script(
                '<script type="text/javascript" characterSet="utf-8" ' \
                'src="/extjs/ext-all-debug.js"></script>')
        else:
            self._root.add_script(
                '<script type="text/javascript" characterSet="utf-8" ' \
                'src="/extjs/adapter/ext/ext-base.js"></script>')
            self._root.add_script(
                '<script type="text/javascript" characterSet="utf-8" ' \
                'src="/extjs/ext-all.js"></script>')

        # Goliat
        if self._options['debug']:
            self._root.add_script(
                '<script type="text/javascript" characterSet="utf-8" ' \
                'src="/goliat/js/Loader.js"></script>')
            self._root.add_script(
                '<script type="text/javascript" characterSet="utf-8">')
            self._root.add_script(
                '    var goliat_loader = new Goliat.Loader();')
            self._root.add_script('    goliat_loader.loadComponents();')
            self._root.add_script('</script>')

        else:
            self._root.add_script(
                '<script type="text/javascript" characterSet="utf-8" ' \
                'src="/goliat/js/goliat-min.js"></script>')

        # ===========================
        # Application main
        # (Coded by User)
        # ===========================
        self._root.add_script(
            '<script type="text/javascript" characterSet="utf-8" ' \
            'src="/js/main.js"></script>')

        # ===========================
        # Application UI
        # ===========================
        for ui_script in self._scripts:
            self._root.add_script(
                '<script type="text/javascript" characterSet="utf-8" ' \
                'src="/ui/{0}"></script>'.format(ui_script))

        # ===========================
        # Resource Modules
        # ===========================        
        for file in self._explore_application():
            module_manager.register(Module(file))

        # Append Resources to the root object        
        for module in module_manager.get_modules():
            self._root.putChild(module.get_url_path(), module.get_module())
            self._modules.append(module.get_name())

        self._modules_loaded=True

        # ===========================
        # Locales
        # ===========================
        self._root.add_script(
            '<script type="text/javascript" characterSet="utf-8" ' \
            'src="/goliat/js/locale/goliat-lang-{0}.js"></script>'.format(
                self._options['locale']))


    def _load_scripts(self):
        """Load scripts and fill scripts application list."""
        for file_name in self._explore_application('script'):
            self._scripts.append(file_name)

    def _load_styles(self):
        """Load styles and fill styles application list."""
        for file_name in self._explore_application('style'):
            self._styles.append(file_name)

    def _explore_application(self, type='module'):
        """Explores the module path directory and returns a filenames tuple."""
        try:
            files=os.listdir('application/view')
            if type=='module':
                files=os.listdir('application/controller')
                pattern=re.compile('[^_?]\.py$', re.IGNORECASE)
            elif type=='script':
                pattern=re.compile('\.js$', re.IGNORECASE)
            elif type=='style':
                files=os.listdir('web/css')
                pattern=re.compile('\.css$', re.IGNORECASE)
            files=filter(pattern.search, files)
            return files
        except OSError:
            return list()

    def _notify(self, wd, filepath, mask):
        """Notifies the changes on application/controller filesystem"""
        if mask is 2:
            if filepath.basename().replace('.py', '') in self._modules:
                self._module_manager.reload(filepath.basename().replace('.py', ''))

        if mask is 256:
            if filepath.exists():
                filename=filepath.basename()
                if len(filename.split('.')) is 2:
                    if filename.split('.')[1]=='py':
                        module=Module(filename)
                        self._module_manager.register(module)
                        self._root.putChild(module.get_url_path(), module.get_module())
                        self._modules.append(module.get_name())

        #print "event %s (%s) on %s"%(
        #    ', '.join(inotify.humanReadableMask(mask)), mask, filepath)
