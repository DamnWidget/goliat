'''
Evoque - managed eval-based freeform templating 
Copyright (C) 2007 Mario Ruggier <mario@ruggier.org>
Licensed under the Academic Free License version 3.0
URL: http://evoque.gizmojo.org/
'''
__url__ = "$URL: svn://gizmojo.org/pub/evoque/trunk/ext/django/evoque_django.py $"
__revision__ = "$Id: evoque_django.py 1058 2008-08-02 16:59:36Z mario $"

# $begin{code}
import sys
from os.path import join, dirname, abspath
import logging
from evoque.domain import Domain
from django.http import HttpResponse

# to add to global namespace
from django.core.paginator import ObjectPaginator
from my_site import formatting_utils

# default template collection root directory
DEFAULT_DIR = abspath(join(dirname(__file__), 'templates'))

# create template domain instance 
# here restating all defaults, for doc convenience
domain = Domain(DEFAULT_DIR,
    restricted=False, errors=3, log=logging.getLogger("evoque"),
    cache_size=0, auto_reload=60, slurpy_directives=True,
    quoting="xml", input_encoding="utf-8", filters=[] )

# adjust global namespace as needed by application
domain.set_on_globals("ObjectPaginator", ObjectPaginator)
domain.set_on_globals("site_name", "mysite.net")
domain.set_namespace_on_globals("formatting_utils", formatting_utils)

# set up any other collection, as needed by application 
# here restating all defaults -- when None, domain's value is used
domain.set_collection("custom", "/home/me/custom_collection/",
    cache_size=None, auto_reload=None, slurpy_directives=None, 
    quoting=None, input_encoding=None, filters=None)


# here we would do any other domain setup we might need
# e.g. set a template default for a given collection
# for details see: http://evoque.gizmojo.org/usage/
# or the source of the evoque.domain module.


def evoque_django_response(request, name, 
        src=None, collection=None, raw=None, data=None, 
        quoting=None, input_encoding=None, filters=None,
        **kwargs):
    """ Render an evoque template to a django response object 
    """
    # get the template, loading it if necessary. 
    # only name is required but all supported options 
    # are passed on for completeness.
    template = domain.get_template(name, src=src, 
        collection=collection, raw=raw, data=data, 
        quoting=quoting, input_encoding=input_encoding, 
        filters=filters)
    # evoque the template and create a django HTTPResponse object:
    # - evoque'ations are always in unicode, so we decode to utf-8
    # - any and all kwargs are added to locals namespace
    return HttpResponse(template.evoque(raw=raw, quoting=quoting, 
                request=request, **kwargs).encode('utf-8'))
