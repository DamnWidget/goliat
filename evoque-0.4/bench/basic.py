'''
Evoque - managed eval-based freeform templating 
Copyright (C) 2007 Mario Ruggier <mario@ruggier.org>
Licensed under the Academic Free License version 3.0
URL: http://evoque.gizmojo.org/
'''
__url__ = "$URL: svn://gizmojo.org/pub/evoque/trunk/bench/basic.py $"
__revision__ = "$Id: basic.py 1138 2009-01-15 17:44:52Z mario $"
#
# Template language benchmarks
#
# Objective: Test general templating features using a small template
# 
# This bench is based on: genshi/examples/bench/basic.py 
# The template sub-folders for genshi, genshi_text and mako are 
# an unmodified copy of those in genshi 0.4.4, and are inlcuded here
# for convenience.

import os
import sys
import timeit

BASEPATH = os.path.abspath(os.path.dirname(__file__))
__all__ = [ 'qpy', 'qpy_eval', 'qpy_ceval', 
            'evoque', 'evoque_mq', 'evoque_nq', 'evoque_r', 
            'mako', 'mako_mq', 'mako_nq', 
            'genshi_text_mq', 'genshi' ]

def pr(*args):
    sys.stdout.write(" ".join([str(arg) for arg in args])+'\n')

# $begin{data}
DATA = dict(title='Just a test', user='joe', 
            items=['<n>%d</n>' % (num)  for num in range(1, 15)])
# $end{data}

# automatic quoting 
def qpy(dirname, verbose=False):
    from qpy_.templates import page
    def render():
        return page(**DATA.copy())
    if verbose:
        pr(render())
    return render

# automatic quoting 
def qpy_eval(dirname, verbose=False):
    from qpy_eval.templates import page, Evaluator
    evaluator = Evaluator()
    def render():
        evaluator.set_locals(DATA.copy())
        return page % evaluator
    if verbose:
        pr(render())
    return render

# automatic quoting 
def qpy_ceval(dirname, verbose=False):
    from qpy_eval.templates import page, CompilingEvaluator
    cevaluator = CompilingEvaluator()
    cevaluator.set_codes(page)
    def render():
        cevaluator.set_locals(DATA.copy())
        return page % cevaluator
    if verbose:
        pr(render())
    return render


# evoque 

# automatic quoting 
def evoque(dirname, verbose=False, quoting="xml", restricted=False):
    DEFAULT_DIR = os.path.join(BASEPATH, 'evoque')
    from evoque.domain import Domain
    td = Domain(DEFAULT_DIR, restricted=restricted, errors=4, quoting=quoting)
    t = td.get_template('template.html')
    t.test()
    def render():
        return t.evoque(DATA.copy())
    if verbose:
        pr(t.ts, render())
    return render

# manual quoting 
def evoque_mq(dirname, verbose=False):
    DEFAULT_DIR = os.path.join(BASEPATH, 'evoque')
    from evoque.domain import Domain
    td = Domain(DEFAULT_DIR, restricted=False, quoting="str")
    import cgi
    td.set_on_globals("quote", cgi.escape) 
    t = td.get_template('template_mq.html')
    t.test()
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
    template = lookup.get_template('template.html')
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
    template = lookup.get_template('template_mq.html')
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
    DEFAULT_DIR = os.path.join(BASEPATH, 'genshi_text')
    from genshi.core import escape
    from genshi.template import TemplateLoader, NewTextTemplate
    loader = TemplateLoader([DEFAULT_DIR], auto_reload=False)
    template = loader.load('template.txt', cls=NewTextTemplate)
    def render():
        return template.generate(escape=escape, **DATA.copy()).render('text')
    if verbose:
        pr(render())
    return render

# genshi xml -- copied here from genshi's basic benchmark, to ensure 
# same data dict as all others tests here. 
# automatic quoting
def genshi(dirname, verbose=False):
    from genshi.template import TemplateLoader
    loader = TemplateLoader([dirname], auto_reload=False)
    template = loader.load('template.html')
    def render():
        return template.generate(**DATA.copy()).render('xhtml')
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

#
# code below is identical to genshi/examples/bench/basic.py :
#

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
