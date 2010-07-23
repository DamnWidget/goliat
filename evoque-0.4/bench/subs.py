'''
Evoque - managed eval-based freeform templating 
Copyright (C) 2007 Mario Ruggier <mario@ruggier.org>
Licensed under the Academic Free License version 3.0
URL: http://evoque.gizmojo.org/
'''
__url__ = "$URL: svn://gizmojo.org/pub/evoque/trunk/bench/subs.py $"
__revision__ = "$Id: subs.py 1138 2009-01-15 17:44:52Z mario $"
#
# Template language benchmarks
#
# Objective: Test string interpolation only

import os
import sys
import timeit

__all__ = [ 'pystr_nq', 'qpy', 
            'evoque', 'evoque_mq', 'evoque_nq', 'evoque_r',
            'mako', 'mako_mq', 'mako_nq',
            'genshi_text_mq'] 

def pr(*args):
    sys.stdout.write(" ".join([str(arg) for arg in args])+'\n')

BASEPATH = os.path.abspath(os.path.dirname(__file__))
# $begin{data}
DATA = dict(title='Your balance', first="Joey", username='joe123', 
    last="2008-02-29", balance=789.19, 
    comment="Thank you <b>very</b> much!")
# $end{data}

# python string.Template - no quoting
def pystr_nq(dirname, verbose=False):
    from string import Template
    src = open(os.path.join(BASEPATH, 'evoque/subs.html')).read()
    template = Template(src)
    def render():
        return template.substitute(**DATA.copy())
    if verbose:
        pr(render())
    return render

# automatic quoting 
def qpy(dirname, verbose=False):
    from qpy_.subs import subs
    def render():
        return subs(**DATA.copy())
    if verbose:
        pr(render())
    return render


# evoque 

# automatic quoting 
def evoque(dirname, verbose=False, quoting="xml", restricted=False):
    DEFAULT_DIR = os.path.join(BASEPATH, 'evoque')
    name = 'subs.html'
    from evoque.domain import Domain
    td = Domain(DEFAULT_DIR, restricted=restricted, errors=4, quoting=quoting)
    t = td.get_template(name)
    def render():
        return t.evoque(DATA.copy())
    if verbose:
        pr(t.ts, render())
    return render

# manual quoting 
def evoque_mq(dirname, verbose=False):
    DEFAULT_DIR = os.path.join(BASEPATH, 'evoque')
    name = 'subs_mq.html'
    from evoque.domain import Domain
    td = Domain(DEFAULT_DIR, restricted=False, quoting="str")
    import cgi
    td.set_on_globals("quote", cgi.escape) 
    t = td.get_template(name)
    def render():
        return t.evoque(DATA.copy())
    if verbose:
        pr(t.ts, render())
    return render

# no quoting 
def evoque_nq(dirname, verbose=False):
    return evoque(dirname, verbose=verbose, quoting="str")

# automatic quoting, restricted execution
def evoque_r(dirname, verbose=False):
    return evoque(dirname, verbose=verbose, restricted=True)


# mako

# automatic quoting 
def mako(dirname, verbose=False, default_filters=['h']):
    from mako.template import Template
    from mako.lookup import TemplateLookup
    lookup = TemplateLookup(directories=[dirname], default_filters=default_filters, 
                            filesystem_checks=False)
    template = lookup.get_template('subs.html')
    def render():
        return template.render(**DATA.copy())
    if verbose:
        pr(template.code, render())
    return render

# manual quoting 
def mako_mq(dirname, verbose=False):
    DEFAULT_DIR = os.path.join(BASEPATH, 'mako')
    from mako.template import Template
    from mako.lookup import TemplateLookup
    lookup = TemplateLookup(directories=[DEFAULT_DIR], filesystem_checks=False)
    template = lookup.get_template('subs_mq.html')
    def render():
        return template.render(**DATA.copy())
    if verbose:
        pr(template.code, render())
    return render

# no quoting 
def mako_nq(dirname, verbose=False):
    DEFAULT_DIR = os.path.join(BASEPATH, 'mako')
    return mako(DEFAULT_DIR, verbose=verbose, default_filters=None)


# genshi 

# manual quoting 
def genshi_text_mq(dirname, verbose=False):
    from genshi.core import escape # from cgi import escape
    from genshi.template import TemplateLoader, NewTextTemplate
    DEFAULT_DIR = os.path.join(BASEPATH, 'evoque')
    loader = TemplateLoader([DEFAULT_DIR], auto_reload=False)
    template = loader.load('subs_mq.html', cls=NewTextTemplate)
    def render():
        return template.generate(quote=escape, **DATA.copy()).render('text')
    if verbose:
        pr(render())
    return render

# 

def run(engine, number=2000, verbose=False):
    for engine in engines:
        # dirname is used by mako, genshi only
        dirname = os.path.join(BASEPATH, engine) 
        engine_name = '%s:%s' % (engine[:16], " "*(15-len(engine)))
        if verbose:
            print
            pr('--------------------------------------------------------')
        t = timeit.Timer(setup='from __main__ import %s; render = %s(r"%s", %s)'
                               % (engine, engine, dirname, verbose),
                         stmt='render()')
        time = t.timeit(number=number) / number
        if verbose:
            pr('--------------------------------------------------------')
        pr(engine_name, '%6.3f ms' % (1000 * time))
        if verbose:
            pr('--------------------------------------------------------')

if __name__ == '__main__':
    engines = [arg for arg in sys.argv[1:] if arg[0] != '-']
    if not engines:
        engines = __all__
    verbose = '-v' in sys.argv
    if '-p' in sys.argv:
        import hotshot, hotshot.stats
        prof = hotshot.Profile("template.prof")
        benchtime = prof.runcall(run, engines, number=100, verbose=verbose)
        stats = hotshot.stats.load("template.prof")
        stats.strip_dirs()
        stats.sort_stats('time', 'calls')
        stats.print_stats(.05)
    else:
        run(engines, verbose=verbose)
