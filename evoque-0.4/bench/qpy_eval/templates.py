'''
Evoque - managed eval-based freeform templating 
Copyright (C) 2007 Mario Ruggier <mario@ruggier.org>
Licensed under the Academic Free License version 3.0
URL: http://evoque.gizmojo.org/
'''
__url__ = "$URL: svn://gizmojo.org/pub/evoque/trunk/bench/qpy_eval/templates.py $"
__revision__ = "$Id: templates.py 1135 2009-01-10 16:42:30Z mario $"

import sys
from qpy import xml

def greeting(name):
    return xml('Hello ') +name+ xml('!')

def header(title):
    return xml('<div id="header"><h1>') +title+ xml('</h1></div>')

footer = xml('<div id="footer"></div>')

def loop (items) :
    s = []
    if items:
        num_items = len(items)
        class_attr = ""
        s.append(xml('<ul>'))
        for i, item in enumerate(items):
            if i+1 == num_items: 
                class_attr = ' class="last"'
            s.append(xml('<li'+class_attr+'>'))
            s.append(item)
            s.append(xml('</li>\n'))
        s.append(xml('</ul>'))
    return xml("").join(s)
    #return qpy.join_xml(s) # slighty slower

# execution context: title, user, items; greeting(user|"name"), loop(items);
page = xml('''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
  <head>
    <title>%(title)s</title>
  </head>
  <body>
  %(header(title))s
  
  <div>%(greeting(user))s</div>
  <div>%(greeting('me'))s</div>
  <div>%(greeting('world'))s</div>

  <h2>Loop</h2>
  %(loop(items))s

  %(footer)s
  </body>
</html>''')

#

class Evaluator(object):
    """ bare-metal evaluator, e.g. no error handling """

    def __init__ (self, globals=globals(), locals=None):
        self.globals = globals
        self.locals = locals or {}

    def __getitem__(self, name):
        return eval(name, self.globals, self.locals)

    def set_locals (self, locals):
        self.locals = locals

class CompilingEvaluator(Evaluator):
    """ bare-metal evaluator, but remembers compiled expressions """

    def __init__ (self, globals=globals(), locals=None):
        Evaluator.__init__(self, globals, locals)
        self.codes = {}

    def __getitem__(self, name):
        try:
            return eval(self.codes[name], self.globals, self.locals)
        except (KeyError,):
            e = sys.exc_info()[1]
            self.codes[name] = compile(name, '<string>', 'eval')
            return self[name] 

    def set_codes(self, s):
        self.codes.clear()
        done = False
        while not done:
            try:
                s % self.codes
                done = True
            except (KeyError,):
                e = sys.exc_info()[1]
                self.codes[e.args[0]] = compile(e.args[0], '<string>', 'eval')

    def get_codenames(self):
        return self.codes.keys()
    
