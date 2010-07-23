'''
Evoque - managed eval-based freeform templating 
Copyright (C) 2007 Mario Ruggier <mario@ruggier.org>
Licensed under the Academic Free License version 3.0
URL: http://evoque.gizmojo.org/
'''
__url__ = "$URL: svn://gizmojo.org/pub/evoque/trunk/ext/qp/echo/slash.py $"
__revision__ = "$Id: slash.py 1103 2008-12-14 18:05:41Z mario $"

# $begin{code}
import sys
from os.path import join, dirname, abspath
import logging
from evoque.domain import Domain

from qp.pub.publish import Publisher
from qp.pub.common import get_request, page
from qp.fill.directory import Directory
from pprint import pformat

class SitePublisher(Publisher):

    configuration = dict(
        http_address=('', 8001),
        as_https_address=('localhost', 9001),
        https_address=('localhost', 10001),
        scgi_address=('localhost', 11001),
    )
    
    def __init__(self, **kwargs):
        super(SitePublisher, self).__init__(**kwargs)
        self.set_domain()
    
    def set_domain(self):
        default_dir = abspath(join(dirname(__file__), 'evoque'))
        # create template domain instance 
        # here restating all defaults, for doc convenience
        self.domain = Domain(default_dir, 
            restricted=False, errors=3, log=logging.getLogger("evoque"),
            cache_size=0, auto_reload=60, slurpy_directives=True, 
            quoting="xml", input_encoding="utf-8", filters=[]
        )
        # extensions to global namespace
        self.domain.set_on_globals("pformat", pformat)
        # preload a default template, e.g. for error pages
        self.domain.get_collection().get_template("", "base.html")
        # other setup e.g. adding other collections, template aliases
        # see: http://evoque.gizmojo.org/usage/
        
    def page(self, title, *content, **kwargs):
        """(title, *content, **kwargs) -> qpy.xml
        Return a page formatted according to the site-standard.
        """
        # we make use of only the "template" kwarg -- there are 
        # other possibilities, see: domain.get_template()
        template = kwargs.get("template", "")
        return self.domain.get_template(template).evoque(
                        title=title, content=content, **kwargs)
        
class SiteDirectory(Directory):
    """
    This site displays the http request.
    """
    
    def get_exports(self):
        yield '', 'index', None, None
    
    def index(self):
        items = get_request().__dict__.items()
        items.sort()
        return page('HTTP Request', template="items.html", items=items)
    
    def _q_traverse(self, components):
        return self.index()
    
