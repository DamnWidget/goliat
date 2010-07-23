'''
Evoque - managed eval-based freeform templating 
Copyright (C) 2007 Mario Ruggier <mario@ruggier.org>
Licensed under the Academic Free License version 3.0
URL: http://evoque.gizmojo.org/
'''
__url__ = "$URL: svn://gizmojo.org/pub/evoque/trunk/test/test_whitespace.py $"
__revision__ = "$Id: test_whitespace.py 1140 2009-01-15 18:26:07Z mario $"

from os.path import abspath, join, dirname
import unittest
from evoque.domain import Domain
from evoque.template import Template

DEFAULT_DIR = abspath(join(dirname(__file__), 'data'))
RESTRICTED = False
ERRORS = 3

class WhitespaceTest(unittest.TestCase):

    context_dict = {
        'title': 'Some <test>',
        'navigation': [
            {'href': '#', 'caption': '<escaping>'},
            {'href': '#', 'caption': 'foobar'},
            {'href': '#', 'caption': 'baz'}
        ],
        'table': [
            [1,2,3,4,5,6,7,8,9,0],
            [1,2,3,4,5,6,7,8,9,0],
            [1,2,3,4,5,6,7,8,9,0],
            [1,2,3,4,5,6,7,8,9,0],
            [1,2,3,4,5,6,7,8,9,0]
        ]
    }
        
    def test_benchsimple_not_slurpy(self):
        target = open(join(DEFAULT_DIR, "benchsimple_result.html"),'r').read()
        td = Domain(DEFAULT_DIR, restricted=RESTRICTED, errors=ERRORS, 
                        slurpy_directives=False)
        t = td.get_template('benchsimple_template.html')
        self.assertEqual(target, t.evoque(self.context_dict))
    
    def test_benchsimple_slurpy(self):
        target = open(join(DEFAULT_DIR, "benchsimple_result.html"),'r').read()
        td = Domain(DEFAULT_DIR, restricted=RESTRICTED, errors=ERRORS)
        t = td.get_template('benchsimple_template_sd.html')
        result = t.evoque(self.context_dict)
        self.assertEqual(target, result)
    
    def test_inline_nested_if(self):
        td = Domain(DEFAULT_DIR, restricted=RESTRICTED, errors=ERRORS)
        t = td.get_template('for_seq_items.html')
        #print t.ts_raw
        #print t.ts
        result = """<ul>
    <li>7:Apples</li>
    <li>9:789</li>
    <li class="last">17:Blue</li>
</ul>
"""
        self.assertEqual(result, t.evoque())
    

if __name__ == '__main__':
    
    unittest.main()
    
