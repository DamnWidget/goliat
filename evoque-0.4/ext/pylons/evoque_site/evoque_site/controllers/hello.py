import logging

from pylons import request, response, session
from pylons import tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from evoque_site.lib.base import BaseController, render
#import evoque_site.model as model

log = logging.getLogger(__name__)

# $begin{ext}
class HelloController(BaseController):

    def index(self):
        # Return a rendered template with evoque 
        c.title = "Hello from evoque!"
        return render("template.html")
# $end{ext}

# this is all OK...
# How best to get "paster controller" generate the render import?
# How best to get "paster create" templating="evoque" fill in all the rest, i.e.
# - to generate the necessary environment code?
# - to not generate unnecessary code (for using other systems)
# - does a pylons application that selects a different templating than the 
#   default incurr any unused & per-request overhead in updating objects 
#   that in this context will always go unused?
# How to declare config params in an ini and use them to initialize the
# evoque domain?