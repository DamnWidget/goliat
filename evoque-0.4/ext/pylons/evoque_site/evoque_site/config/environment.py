"""Pylons environment configuration"""
import os

from pylons import config

import evoque_site.lib.app_globals as app_globals
import evoque_site.lib.helpers
from evoque_site.config.routing import make_map

def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
    # Pylons paths
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root,
                 controllers=os.path.join(root, 'controllers'),
                 static_files=os.path.join(root, 'public'),
                 templates=[os.path.join(root, 'templates')])

    # Initialize config with the basic options
    config.init_app(global_conf, app_conf, package='evoque_site', paths=paths)

    config['routes.map'] = make_map()
    config['pylons.app_globals'] = app_globals.Globals()
    config['pylons.h'] = evoque_site.lib.helpers
    
    # $begin{ext} ##
    # Evoque Templating: 
    # http://evoque.gizmojo.org/ext/pylons/
    # http://evoque.gizmojo.org/usage/api/
    
    import logging
    from evoque.domain import Domain
    
    evoque_domain = Domain(
        # root folder for the default template collection, must be abspath;
        # as default use pylon's first templates folder
        os.path.join(root, 
                app_conf.get("evoque.default_dir") or paths['templates'][0]),
        
        # whether evaluation namespace is restricted or not 
        restricted = app_conf.get("evoque.restricted")=="true",    
        
        # how should any evaluation errors be rendered
        # int 0 to 4, for: [silent, zero, name, render, raise]
        errors = int(app_conf.get("evoque.errors", 3)),
        
        # evoque logger; additional setings should be specified via the pylons
        # config ini file, just as for any other logger in a pylons application
        log = logging.getLogger("evoque"), 
        
        # [collections] int, max loaded templates in a collection
        cache_size = int(app_conf.get("evoque.cache_size", 0)), 
        
        # [collections] int, min seconds to wait between checks for
        # whether a template needs reloading
        auto_reload = int(app_conf.get("evoque.auto_reload", 60)), 
        
        # [collections] bool, consume all whitespace trailing a directive
        slurpy_directives = app_conf.get("evoque.slurpy_directives")=="true",
        
        # [collections/templates] str or class, to specify the *escaped* 
        # string class that should be used i.e. if any str input is not of 
        # this type, then cast it to this type). 
        # Builtin str key values are: "xml" -> qpy.xml, "str" -> unicode
        quoting = app_conf.get("evoque.quoting", "xml"),
        
        # [collections/templates] str, preferred encoding to be tried 
        # first when decoding template source. Evoque decodes templates 
        # strings heuristically, i.e. guesses the input encoding.
        input_encoding = app_conf.get("evoque.input_encoding", "utf-8"),
        
        # [collections/templates] list of filter functions, each having 
        # the following signature: filter_func(s:basestring) -> basestring
        # The functions will be called, in a left-to-right order, after 
        # template is rendered. NOTE: not settable from the conf ini.
        filters=[]
    )
    
    # default template (optional) i.e. what to receive
    # when calling domain.get_template() with no params
    if app_conf.get("evoque.default_template"):
        evoque_domain.get_collection().get_template("", 
                src=app_conf.get("evoque.default_template"))
    
    # attach evoque domain to app_globals
    config['pylons.app_globals'].evoque_domain = evoque_domain 
    ## $end{ext}    
    evoque_domain.log.debug(evoque_domain.__dict__)
    
    # CONFIGURATION OPTIONS HERE (note: all config options will override
    # any Pylons config options)

