"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController

class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']

        return WSGIController.__call__(self, environ, start_response)

# $begin{ext}
from pylons.templating import pylons_globals, cached_template

def render_evoque(template_name, extra_vars=None, cache_key=None,
                    cache_type=None, cache_expire=None,
                    collection=None, raw=False, quoting=None):
    """ Render a template with Evoque : http://evoque.gizmojo.org/ext/pylons/
	
    Accepts the cache options ``cache_key``, ``cache_type``, and
    ``cache_expire``. 
    
    The remaining options affect how template is located, loaded and rendered:
    - template_name: normally this is the collection-root-relative locator for
          the template; if template had been previously with location specified
          via the src option, then may be any arbitrary string identifier.
    - collection: either(None, str, Collection), an existing collection, 
          None implies the default collection
    - raw: bool, render the raw template source 
    - quoting: either(str, type), sets the Quoted-No-More string class to use, 
          None uses the collection's default, 
          "xml" uses qpy.xml, 
          "str" uses unicode
    """
    # Create a render callable for the cache function
    def render_template():
        # Get the globals
        # Note: when running in restricted mode which of these globals are
        # to be exposed should be a lot more selective. 
        pg = pylons_globals()
        
        # Update any extra vars if needed
        if extra_vars:
            pg.update(extra_vars)
        
        # Grab a template reference
        template = pg['app_globals'].evoque_domain.get_template(
            template_name, collection=collection, raw=raw, quoting=quoting)
        return template.evoque(pg, raw=raw, quoting=quoting)
    
    return cached_template(template_name, render_template, cache_key=cache_key,
                    cache_type=cache_type, cache_expire=cache_expire)

render = render_evoque
# $end{ext}
