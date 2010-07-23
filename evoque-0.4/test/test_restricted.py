'''
Evoque - managed eval-based freeform templating 
Copyright (C) 2007 Mario Ruggier <mario@ruggier.org>
Licensed under the Academic Free License version 3.0
URL: http://evoque.gizmojo.org/
'''
__url__ = "$URL: svn://gizmojo.org/pub/evoque/trunk/test/test_restricted.py $"
__revision__ = "$Id: test_restricted.py 1151 2009-01-20 01:50:54Z mario $"

from os.path import abspath, join, dirname
import unittest
from evoque.domain import Domain, DISALLOW_BUILTINS
from evoque.collection import Collection
from evoque.template import Template
from evoque.evaluator import StringIO

import logging
logging_level = logging.CRITICAL # hide the plentiful ERROR logs

DEFAULT_DIR = abspath(join(dirname(__file__), 'data'))

# Attempt at accessing these attrs under restricted execution on an object 
# that has them should raise a RuntimeError
RESTRICTED_ATTRS = [
    'im_class', 'im_func', 'im_self', 'func_code', 'func_defaults', 
    'func_globals', 'func_name', 
    'tb_frame', 'tb_next', 
    'f_back', 'f_builtins', 'f_code', 'f_exc_traceback', 'f_exc_type', 
    'f_exc_value', 'f_globals', 'f_locals'
]

class RestrictedTest(unittest.TestCase):
    
    def __init__(self, *args, **kw):
        super(RestrictedTest, self).__init__(*args, **kw)
        self.domain = Domain(DEFAULT_DIR, restricted=True, errors=4)
        self.domain.log.setLevel(logging_level)
        self.count = 0

    def get_template_from_expr(self, expr):
        self.count += 1
        name = "tfs%s" % (self.count)
        src = "${%s}" % (expr)
        self.domain.set_template(name, src=src, from_string=True)
        return self.domain.get_template(name)
    
    def test_restricted(self):
        for bi in DISALLOW_BUILTINS:
            t = self.get_template_from_expr(bi)
            self.assertRaises((LookupError, NameError), t.evoque)
    
    def test_inquisitive(self):
        # on a function object, evoque()
        for expr in [ "evoque."+attr for attr in RESTRICTED_ATTRS ]:
            t = self.get_template_from_expr(expr)
            self.assertRaises((LookupError,), t.evoque)
        # on a function object, evoque(), with space between "." and attr name
        for expr in [ "evoque.    "+attr for attr in RESTRICTED_ATTRS ]:
            t = self.get_template_from_expr(expr)
            self.assertRaises((LookupError,), t.evoque)

    def test_unsafe_str_expressions(self):
        # NameError, unsafe builtins
        for expr in [
            "open('test.txt', 'w')",
            "getattr(int, '_' + '_abs_' + '_')",
            ]:
            t = self.get_template_from_expr(expr)
            self.assertRaises((NameError,), t.evoque)
        # LookupError
        for expr in [
            # lowlevel tricks to access 'object'
            "().__class__.mro()[1].__subclasses__()", 
            "type(1)._" + "_abs_" + "_",
            "()."+"_"*2+"class"+"_"*2+".mro()[1]."+"_"*2+"subclasses"+"_"*2+"()", 
            ]:
            t = self.get_template_from_expr(expr)
            self.assertRaises((LookupError,), t.evoque)
        # SyntaxError
        for expr in [
            # attempt to access global enviroment where fun was defined
            "def x(): pass; print x.func_globals", # statement, SyntaxError
            # attempt to execute code which never terminates
            "while 1: pass", # statement, SyntaxError
            ]:
            t = self.get_template_from_expr(expr)
            self.assertRaises((LookupError, SyntaxError,), t.evoque)
        # RuntimeError
        # http://groups.google.com/group/comp.lang.python/browse_thread/thread/689ea92183b91f06
        for expr in [
            # Mark Wooding
            "inspect.func_globals['_'*2+'builtins'+'_'*2].open('"+__file__+"').read()",
            "inspect.func_globals['_'*2+'builtins'+'_'*2]",
            # Daniel Diniz
            "(x for x in ()).throw('bork'),"
            "(x for x in range(1)).gi_frame.f_globals.clear()",
            #"open('where_is_ma_beer.txt', 'w').write('Thanks for the fun')",            
            ]:
            t = self.get_template_from_expr(expr)
            self.assertRaises((LookupError, RuntimeError, AttributeError), t.evoque)
        
    def test_unsafe_file_expressions(self):
        # Create a new domain for this, to be able to run with a different 
        # errors setting
        td = Domain(DEFAULT_DIR, restricted=True, errors=2, quoting="str")
        name = 'restricted_exprs.txt'
        t = td.get_template(name)
        result = """
  [EvalError(().__class__.mro()[1].__subclasses__())]
  ().__class__.mro()[1].__subclasses__()
  ().__class__.mro()[1].__subclasses__()
  [EvalError(eval(expr))]
  [EvalError(evoque("test", src="${"+expr+"}", from_string=True))]
"""
        self.assertEqual(result, t.evoque())


if __name__ == '__main__':
    
    unittest.main()
    
