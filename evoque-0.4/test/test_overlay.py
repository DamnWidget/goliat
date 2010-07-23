'''
Evoque - managed eval-based freeform templating 
Copyright (C) 2007 Mario Ruggier <mario@ruggier.org>
Licensed under the Academic Free License version 3.0
URL: http://evoque.gizmojo.org/
'''
__url__ = "$URL: svn://gizmojo.org/pub/evoque/trunk/test/test_overlay.py $"
__revision__ = "$Id: test_overlay.py 1111 2008-12-30 08:51:05Z mario $"

from os.path import abspath, join, dirname
import unittest
from evoque.domain import Domain
from evoque.template import Template

DEFAULT_DIR = abspath(join(dirname(__file__), 'data'))

class OverlayTest(unittest.TestCase):

    def test_overlay(self):
        td = Domain(DEFAULT_DIR)
        t = td.get_template('overlay.html')
        self.assertEqual(
                eval("dict(%s)"%(t.eval_overlay)), dict(name="base.html"))
        space, overlay = t.get_space_overlay()
        self.failUnless(space is True)
        self.failUnless(t.labels == ["content"])
        # t.evoque(title="positive overlay test", parametrized="and happy")
        
        chain_pos = td.get_template('overlay_chain_pos.html')
        self.assertEqual(
            eval("dict(%s)"%(chain_pos.eval_overlay)), dict(name="overlay_mid.html"))
        space, overlay = chain_pos.get_space_overlay()
        self.failUnless(space is True)
        self.failUnless(chain_pos.labels == ["content"])
        # chain_pos.evoque(title="positive overlay test", parametrized="and happy")
        
        chain_neg = td.get_template('overlay_chain_neg.html')
        self.assertEqual(eval("dict(%s)"%(chain_neg.eval_overlay)), 
            dict(name="overlay_mid.html", space="negative"))
        space, overlay = chain_neg.get_space_overlay()
        self.failUnless(space is False)
        self.failUnless(chain_neg.labels == ["content", "footer"])
        # chain_neg.evoque(title="negative overlay test", parametrized="and happy")
        
        b = td.get_template('base.html')
        self.failUnless(b.labels == ["header", "content", "footer"])
        self.failIf(b.eval_overlay is not None)
        self.assertRaises((TypeError,), b.get_space_overlay)
        # b.evoque(title="negative overlay test", parametrized="and happy")
        
    def test_dynamic_site_template(self):
        domain = Domain(DEFAULT_DIR)
        #
        # by reset
        s = domain.get_template("SITE-TEMPLATE", src="site_template_table.html")
        t = domain.get_template("site_dyn_page.html")
        r_table = t.evoque(
            title="hey tabby!", message="you're kinda square!", footer="you reckon?")
        self.failUnless(r_table == """<html>
<head><title>site-table: hey tabby!</title></head>
<body>
    <table class="layout">
        <tr><th>site-table: <h1>hey tabby!</h1></th></tr>
        <tr><td>page: you&#39;re kinda square!</td></tr>
        <tr><td>site-table: you reckon?</td></tr>
    </table>
</body>
</html>
""")
        s.unload()
        s = domain.get_template("SITE-TEMPLATE", src="site_template_divs.html")
        r_divs = t.evoque(
            title="howdie!", message="ya bin free floatin' good?", footer="sure thang!")
        self.failUnless(r_divs == """<html>
<head><title>site-div: howdie!</title></head>
<body>
    <div class="layout">
        <div class="header">site-div: <h1>howdie!</h1></div>
        <div class="content">page: ya bin free floatin&#39; good?</div>
        <div class="footer">site-div: sure thang!</div>
    </div>
</body>
</html>
""")
        # by parameter
        t = domain.get_template("site_dyn_page_var.html")
        self.assertEqual(r_table, t.evoque(my_site_theme="site_template_table.html",
            title="hey tabby!", message="you're kinda square!", footer="you reckon?"))
        self.assertEqual(r_divs, t.evoque(my_site_theme="site_template_divs.html",
            title="howdie!", message="ya bin free floatin' good?", footer="sure thang!"))
    
    def test_overlay_naming_schemes_separate_files(self):
        domain = Domain(DEFAULT_DIR)
        t0 = domain.get_template("overlay_naming_base.html")
        self.assertEqual(t0.evoque(), "<base>base content!</base>")
        t1 = domain.get_template("overlay_naming_1.html")
        self.assertEqual(t1.evoque(), "<base><m1>literal unquoted</m1></base>")
        t2 = domain.get_template("overlay_naming_2.html")
        self.assertEqual(t2.evoque(), "<base><m2>literal quoted</m2></base>")
        t3 = domain.get_template("overlay_naming_3.html")
        self.assertEqual(t3.evoque(site_template="overlay_naming_base.html"), 
            "<base><m3>kw unquoted</m3></base>")
        t4 = domain.get_template("overlay_naming_4.html")
        self.assertEqual(t4.evoque(), "<base><m4>kw quoted</m4></base>")
    #+ add similar test case for all templates in same file (currently fails)
    #+ add similar test case for all templates in same file, with an explicitly 
    #  named BASE template e.g.
    #  domain.set_template("BASE", src="overlay_naming_base.html", from_string=False)

    def test_overlay_kwargs(self):
        td = Domain(DEFAULT_DIR)
        r = "<base>base content!</base>"
        r_neg = ""
        responses = [ r, r, r, r, r_neg ]
        t = td.get_template('overlay_kwargs.html')
        for i, s in enumerate(t.test()):
            self.assertEqual(responses[i], s)
    

if __name__ == '__main__':
    unittest.main()

