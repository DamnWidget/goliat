'''
Evoque - managed eval-based freeform templating 
Copyright (C) 2007 Mario Ruggier <mario@ruggier.org>
Licensed under the Academic Free License version 3.0
URL: http://evoque.gizmojo.org/
'''
__url__ = "$URL: svn://gizmojo.org/pub/evoque/trunk/bench/bigtable.py $"
__revision__ = "$Id: bigtable.py 1152 2009-01-20 10:01:32Z mario $"
#
# Template language benchmarks
#
# Objective: Generate a 1000x10 HTML table as fast as possible.
# (similar to the one in: genshi/examples/bench/bigtable.py)

import os
import sys
import timeit

def pr(*args):
    sys.stdout.write(" ".join([str(arg) for arg in args])+'\n')

BASEDIR = os.path.abspath(os.path.dirname(__file__))
# $begin{data}
BASEROW = ("a","b","c","d","<escape-me/>","f","g","h","i","j")
TABLE_DATA = [ BASEROW for x in range(1000) ]
# $end{data}

__all__ = ['qpy', 
           'evoque', 'evoque_mq', 'evoque_nq', 'evoque_nqt', 'evoque_r', 
           'mako', 'mako_mq', 'mako_nq', 'mako_nqt', 
           'genshi']

# automatic quoting 
def qpy(verbose=False):
    from qpy_.bigtable import bigtable
    def render():
        return bigtable(TABLE_DATA)
    if verbose:
        pr(render()[:300] + "...")
    return render


# evoque 

# automatic quoting 
def evoque(verbose=False, quoting="xml", restricted=False, template_string=None):
    from evoque.domain import Domain
    DEFAULT_DIR = os.path.join(BASEDIR, 'evoque')
    td = Domain(DEFAULT_DIR, restricted=restricted, errors=4, quoting=quoting)
    if template_string is None: 
        # $begin{evoque_template}
        template_string = """<table>
$for{ row in table }
<tr>$for{ col in row }<td>${col}</td>$rof</tr>
$rof
</table>
$test{ table=[("a","b","c","d","<escape-me/>","f","g","h","i","j")] }
"""     # $end{evoque_template}
    td.set_template("bigtable", src=template_string, quoting=quoting)
    t = td.get_template("bigtable")
    t.test()
    def render():
        return t.evoque({'table':TABLE_DATA})
    if verbose:
        #open("/tmp/evoque_bench_bigtable_evoque.html", "w").write(render())
        pr(t.ts)
        pr('--------------------------------------------------------')
        pr(render()[:300] + "...")
    return render

# manual quoting 
def evoque_mq(verbose=False):
    from evoque.domain import Domain
    DEFAULT_DIR = os.path.join(BASEDIR, 'evoque')
    td = Domain(DEFAULT_DIR)
    import cgi
    td.set_on_globals("quote", cgi.escape) 
    template_string = """<table>
$for{ row in table }
<tr>$for{ col in row }<td>${quote(col)}</td>$rof</tr>
$rof
</table>
$test{ table=[("a","b","c","d","<escape-me/>","f","g","h","i","j")] }
"""
    td.set_template("bigtable", src=template_string, quoting="str", 
            from_string=True)
    t = td.get_template("bigtable")
    def render():
        return t.evoque({'table':TABLE_DATA})
    if verbose:
        pr(t.ts)
        pr('--------------------------------------------------------')
        pr(render()[:300] + "...")
    return render

# no quoting 
def evoque_nq(verbose=False):
    return evoque(verbose=verbose, quoting="str")

# no quoting tweaked
def evoque_nqt(verbose=False):
    template_string = """<table>
${ "".join([ "<tr>%s</tr>" %("".join(["<td>%s</td>"%(col) for col in row]))
              for row in table ]) }
</table>
$test{ table=[("a","b","c","d","<escape-me/>","f","g","h","i","j")] }
"""
    return evoque(verbose=verbose, quoting="str", template_string=template_string)

# automatic quoting, restricted execution
def evoque_r(verbose=False):
    return evoque(verbose=verbose, restricted=True)


# mako 

# automatic quoting 
def mako(verbose=False, default_filters=['h']):
    from mako.template import Template
    template = Template("""<table>
% for row in table:
<tr>
% for col in row: 
<td>${col}</td>
% endfor
</tr>
% endfor 
</table>
""", default_filters=default_filters)
    def render():
        return template.render(table=TABLE_DATA)
    if verbose:
        pr(render()[:300] + "...")
        pr('--------------------------------------------------------')
        pr(template.code)
    return render

# manual quoting 
def mako_mq(verbose=False):
    from mako.template import Template
    template = Template("""<table>
% for row in table:
<tr>
% for col in row: 
<td>${col | h}</td>
% endfor
</tr>
% endfor 
</table>
""")
    def render():
        return template.render(table=TABLE_DATA)
    if verbose:
        pr(render()[:300] + "...")
        pr('--------------------------------------------------------')
        pr(template.code)
    return render

# no quoting 
def mako_nq(verbose=False):
    return mako(verbose=verbose, default_filters=None)

# no quoting tweaked
def mako_nqt(verbose=False):
    from mako.template import Template
    template = Template("""<table>
${ "".join([ "<tr>%s</tr>" %("".join(["<td>%s</td>"%(col) for col in row]))
                  for row in table ]) }    
</table>
""")
    def render():
        return template.render(table=TABLE_DATA)
    if verbose:
        pr(render()[:300] + "...")
        pr('--------------------------------------------------------')
        pr(template.code)
    return render


# genshi

# automatic quoting 
def genshi(verbose=False):
    from genshi.template import MarkupTemplate
    genshi_tmpl = MarkupTemplate("""
<table xmlns:py="http://genshi.edgewall.org/">
<tr py:for="row in table">
<td py:for="c in row" py:content="c"/>
</tr>
</table>
""")
    def render():
        stream = genshi_tmpl.generate(table=TABLE_DATA)
        return stream.render('html', strip_whitespace=False)
    if verbose:
        pr(render()[:300] + "...")
    return render

#

def run(engine, number=10, verbose=False):
    for engine in engines:
        engine_name = '%s:%s' % (engine[:16], " "*(15-len(engine)))
        if verbose:
            pr('--------------------------------------------------------')
        t = timeit.Timer(setup='from __main__ import %s; render = %s(%s)'
                               % (engine, engine, verbose),
                         stmt='render()')
        time = t.timeit(number=number) / number
        if verbose:
            pr('--------------------------------------------------------')
        pr(engine_name, '%6.2f ms' % (1000 * time))
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
        benchtime = prof.runcall(run, engines, number=1)
        stats = hotshot.stats.load("template.prof")
        stats.strip_dirs()
        stats.sort_stats('time', 'calls')
        stats.print_stats()
    else:
        run(engines, number=10, verbose=verbose)
