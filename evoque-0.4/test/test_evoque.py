'''
Evoque - managed eval-based freeform templating 
Copyright (C) 2007 Mario Ruggier <mario@ruggier.org>
Licensed under the Academic Free License version 3.0
URL: http://evoque.gizmojo.org/
'''
__url__ = "$URL: svn://gizmojo.org/pub/evoque/trunk/test/test_evoque.py $"
__revision__ = "$Id: test_evoque.py 1140 2009-01-15 18:26:07Z mario $"

import sys
import unittest
from os.path import abspath, join, dirname

from evoque.domain import Domain
from evoque.collection import Collection
from evoque.template import Template, parse_locator
from evoque.evaluator import unistr

def pr(*args):
    sys.stdout.write(" ".join([str(arg) for arg in args])+'\n')

try:
    from qpy import xml
except ImportError:
    xml = None
    pr("No qpy package installed - tests requiring qpy.xml will be skipped.")    

DEFAULT_DIR = abspath(join(dirname(__file__), 'data'))
RESTRICTED = False
ERRORS = 3

from test_restricted import RestrictedTest
from test_overlay import OverlayTest
from test_whitespace import WhitespaceTest
from test_decodeh import DecodehTest

class EvoqueTest(unittest.TestCase):
    
    def setUp(self):
        pass
    def tearDown(self):
        pass
        
    def test_none_dir(self):
        td = Domain(DEFAULT_DIR, restricted=RESTRICTED, errors=ERRORS)
        self.failUnless(isinstance(td.collections[""], Collection))
        self.assertEqual(td.collections[""].name, "")
    
    def test_typical_usage_via_domain_implied_collection(self):
        td = Domain(DEFAULT_DIR, restricted=RESTRICTED, errors=ERRORS)
        name = 'template.html'
        t = td.get_template(name)
        self.failUnless(t.collection is td.get_collection())
        self.failUnless(t.collection is td.collections[""])
        self.failUnless(t is t.collection.get_template(name))
        self.failUnless(t is t.collection.domain.get_template(name, 
                collection=t.collection))
    
    def test_direct_implied_domain_collection(self):
        collection_name = "mycollection"
        tc = Collection(None, collection_name, DEFAULT_DIR)
        td = tc.domain
        name = 'template.html'
        t = Template(tc.domain, name)
        self.failUnless(tc is t.collection)
        self.failUnless(tc is td.get_collection())
        self.assertEqual(tc.name, collection_name)
    
    def test_non_empty_default_collection(self):
        name = 'template.html'
        t = Template(DEFAULT_DIR, name)
        self.failUnless(isinstance(t.collection.domain, Domain))
        self.failUnless(t.collection.domain.collections[""] is t.collection)
        self.failUnless(t is t.collection.get_template(name))
        self.failUnless(t is t.collection.domain.get_template(name, 
                collection=t.collection))
        self.assertRaises((ValueError,), Template, t.collection.domain, name)
    
    def test_empty_default_template(self):
        name = ""
        src = "template.html"
        t = Template(DEFAULT_DIR, name, src)
        self.failUnless(t is t.collection.get_template())
    
    def test_name_and_src_w_frag_template(self):
        name = "named"
        src = "template.html#label"
        t = Template(DEFAULT_DIR, name, src)
        data = dict(title="A Title", param="A Param")
        r = "<h1>A Title</h1><p>some A Param text</p>"
        self.assertEqual(r, t.evoque(**data))

    def test_parse_locator(self):
        td = Domain(DEFAULT_DIR, restricted=RESTRICTED, errors=ERRORS)
        name = "template.html"
        name_label = "template.html#label"
        label = "#label"
        t = td.get_template(name)
        self.assertEqual(["template.html", None], parse_locator(name))
        self.assertEqual(["template.html", "label"], parse_locator(name_label))
        self.assertEqual(["", "label"], parse_locator(label))
        self.assertRaises((ValueError,), parse_locator, "template.html#label#label")
    
    def test_from_string_td(self):
        td = Domain(DEFAULT_DIR, restricted=RESTRICTED, errors=ERRORS)
        src = "<h1>${title}</h1><p>some ${param} text</p>"
        data = dict(title="A Title", param="A Param")
        r = "<h1>A Title</h1><p>some A Param text</p>"
        td.set_template("fromstr", src=src, from_string=True)
        t = td.get_template("fromstr")
        self.assertEqual(r, t.evoque(**data))
    
    def test_from_string(self):
        src = "<h1>${title}</h1><p>some ${param} text</p>"
        data = dict(title="A Title", param="A Param")
        r = "<h1>A Title</h1><p>some A Param text</p>"
        t = Template(DEFAULT_DIR, "fromstr", src=src, from_string=True)
        self.assertEqual(r, t.evoque(**data))
    
    def test_evoque_nested_direct(self):
        name = "template.html#label"
        t = Template(DEFAULT_DIR, name)
        r = "<h1>A Title</h1><p>some A Param text</p>"
        self.assertEqual(r, t.evoque(title="A Title", param="A Param"))
    
    def test_evoque_local_nested(self):
        td = Domain(DEFAULT_DIR, restricted=RESTRICTED, errors=ERRORS)
        name = 'evoque_local_nested.html'
        data = dict(title="A Title", param="A Param")
        r = "<h1>A Title</h1><p>some A Param text</p>"
        # Load a nested template and evoque it
        t1 = td.get_template(name + "#label")
        self.assertEqual(t1.ts, "<h1>%(title)s</h1><p>some %(param)s text</p>")
        self.assertEqual(r, t1.evoque(**data))
        # Load a template that evoques a locally-nested template
        t2 = td.get_template(name)
        self.assertEqual(r, t2.evoque(**data))
    
    def test_get_mixed_name_src(self):
        td = Domain(DEFAULT_DIR, restricted=RESTRICTED, errors=ERRORS)
        name = '#label'
        src = 'evoque_local_nested.html'
        # Load a nested template and evoque it
        t = td.get_template(name, src)
        self.assertEqual(t.ts, "<h1>%(title)s</h1><p>some %(param)s text</p>")

    def test_evoque_raw(self):
        td = Domain(DEFAULT_DIR, restricted=RESTRICTED, errors=ERRORS)
        name = 'evoque_local_nested.html#label'
        r = "<h1>${title}</h1><p>some ${param} text</p>"
        t = td.get_template(name, raw=True)
        self.assertEqual([], list(t.test()))
        self.assertEqual(None, t.ts)
        self.assertEqual(r, t.evoque(raw=True))
        self.assertEqual(r, t.evoque())

    def test_evoque_local_nested_from_string(self):
        td = Domain(DEFAULT_DIR, restricted=RESTRICTED, errors=ERRORS)
        src = open(join(DEFAULT_DIR, "evoque_local_nested.html")).read()
        name = "fromstr"
        nested_name = name + "#label"
        data = dict(title="A Title", param="A Param")
        r = "<h1>A Title</h1><p>some A Param text</p>"
        # Load a from_string template that locally-nests another template
        td.set_template(name, src=src, from_string=True)
        t1 = td.get_template(name)
        # Verify nested template is not yet loaded
        self.assertEqual(False, t1.collection.has_template(nested_name))
        # Evoque, and verify response (multiple times, ensure data stays ok)
        self.assertEqual(r, t1.evoque(data)) # data as locals
        self.assertEqual(r, t1.evoque(**data)) # data as kw
        self.assertEqual(r, t1.evoque(data)) # data as locals
        self.assertEqual(r, t1.evoque(**data)) # data as kw
        # Verify nested template is now loaded
        self.assertEqual(True, t1.collection.has_template(nested_name))
        # Verify that tring to set nested template will fail
        self.assertRaises((ValueError,), td.set_template, nested_name, 
                src=src, from_string=True)
        t2 = td.get_template(nested_name)
        self.assertEqual(t2.ts, "<h1>%(title)s</h1><p>some %(param)s text</p>")
        self.assertEqual(r, t2.evoque(**data))
        
    r_xml_escaped = "<h1>q-xml</h1><p>some &lt;in&gt;rm *&lt;/in&gt; text</p>"
    def test_xml_automatic_quoting(self):
        if not xml: 
            return 
        td = Domain(DEFAULT_DIR, restricted=RESTRICTED, errors=ERRORS, quoting="xml")
        name = "template.html#label"
        t = td.get_template(name)
        self.failUnless(xml is t.qsclass)
        self.failUnless(xml is t.evoque(title="xml", param="<xml/>").__class__)
        self.assertEqual(self.r_xml_escaped, 
                t.evoque(title="q-xml", param="<in>rm *</in>"))
        r = "<h1>q-xml</h1><p>some <in>rm *</in> text</p>"
        self.assertEqual(r, t.evoque(title="q-xml", param=xml("<in>rm *</in>")))
    
    def test_xml_manual_quoting(self):
        if not xml: 
            return 
        td = Domain(DEFAULT_DIR, restricted=RESTRICTED, errors=ERRORS, quoting="str")
        name = "template.html#label"
        t = td.get_template(name)
        self.failUnless(unistr is t.qsclass)
        self.failUnless(unistr is t.evoque(title="str", param="<str/>").__class__)
        from cgi import escape
        self.assertEqual(self.r_xml_escaped, 
                t.evoque(title="q-xml", param=escape("<in>rm *</in>")))
    
    def test_manual_quoting(self):
        td = Domain(DEFAULT_DIR, restricted=RESTRICTED, errors=ERRORS, quoting="str")
        name = "template.html#label"
        t = td.get_template(name)
        self.failUnless(unistr is t.qsclass)
        self.failUnless(unistr is t.evoque(title="str", param="<str/>").__class__)
        from cgi import escape
        self.assertEqual(self.r_xml_escaped, 
                t.evoque(title="q-xml", param=escape("<in>rm *</in>")))
    
    def test_literals(self):
        td = Domain(DEFAULT_DIR, restricted=RESTRICTED, errors=ERRORS)
        name = "template.html"
        t = td.get_template(name + "#literals")
        r = "<p>a $ dollar, a literal ${expr}, a % percent... { } ! \ etc.</p>"
        self.assertEqual(r, t.evoque())
        self.assertRaises((SyntaxError,), td.get_template, name+"#unescaped")
    
    def test_unpack_symbol(self):
        from evoque.translate import unpack_symbol
        symbols = [
            ("a", "a"), 
            ("a, b", ("a", "b")), 
            ("(a, b)", ("a", "b")), 
            ("[a, b]", ["a", "b"]), 
            ("[a, b, (c, d)]", ["a", "b", ("c", "d")]),
            ("[a, b, (c, [one, two, three], d)]", 
                    ["a", "b", ("c", ["one", "two", "three"], "d")])
        ]
        for s, u in symbols:
            self.assertEqual(u, unpack_symbol(s))

    def test_extract_test_data(self):
        td = Domain(DEFAULT_DIR, restricted=RESTRICTED, errors=ERRORS)
        name = "template.html"
        t = td.get_template(name)
        self.assertEqual(t.test_data, [
            dict(title="A Title", param="a <param/> for quoting",
                things=["Apples", 789, "Blue"], something=False, other=False,
                someexpr='abc', likes_blue=False, flag="Banana", yo="Johnny"),
            dict(things=[]),
            dict(something=True),
            dict(something=False, other=True),
            dict(other=False, likes_blue=True) ])

    def test_svn_keywords(self):
        td = Domain(DEFAULT_DIR, restricted=RESTRICTED, errors=ERRORS)
        src = "%s %s" %(__url__, __revision__)
        td.set_template("svnkw", src=src, from_string=True)
        self.assertEqual(src, td.get_template("svnkw").evoque())

    def test_file_addressing_collection_root_relative(self):
        td = Domain(DEFAULT_DIR, restricted=RESTRICTED, errors=ERRORS)
        name = '/template.html'
        src = '/template.html'
        self.assertRaises((LookupError,), td.get_template, name)
        self.assertRaises((LookupError,), td.get_template, name, src)
        # can have names start with "/" as long as the c-rel locator does not
        src = 'template.html'
        t = td.get_template(name, src=src)
        self.assertEqual(t.name, name) 
    
    def test_file_addressing_non_existant(self):
        td = Domain(DEFAULT_DIR, restricted=RESTRICTED, errors=ERRORS)
        name = 'xxx-template.html'
        src = 'xxx-template.html'
        self.assertRaises((ValueError,), td.get_template, name)
        self.assertRaises((ValueError,), td.get_template, name, src)
    
    def test_raw_nested(self):
        if not xml:
            return 
        td = Domain(DEFAULT_DIR, restricted=RESTRICTED, errors=ERRORS)
        t = td.get_template('raw_nested.html')
        self.assertEqual(t.evoque()[:87], """
$begin{table_row}
    $for{ col in row }
        &lt;td&gt;${col}&lt;/td&gt;
    $else""")
        self.failUnless(isinstance(t.evoque(), xml))
        # template #snapshot is already loaded with raw=True, quoting=str
        snap = td.get_template('raw_nested.html#snapshot')
        self.failUnless(snap.raw)
        self.failUnless(snap.qsclass is unistr)
        self.failUnless(isinstance(snap.evoque(), unistr))
        # template #snapshot is still already loaded...
        snapx = td.get_template('raw_nested.html#snapshot_xml')
        self.failUnless(isinstance(snapx.evoque(), xml))
        self.failUnless(snap.qsclass is unistr)
        self.failUnless(isinstance(snap.evoque(), unistr))
        snap.unload()
        self.failUnless(isinstance(snapx.evoque(), xml)) # reloads #snapshot
        snap = td.get_template('raw_nested.html#snapshot')
        self.failUnless(snap.qsclass is xml)
        self.failUnless(isinstance(snap.evoque(raw=True), xml))
        
    def test_prefer(self):
        td = Domain(DEFAULT_DIR, restricted=RESTRICTED, errors=ERRORS)
        t = td.get_template('raw_nested.html')
        self.assertEqual(t.prefer, dict(raw=False, quoting="xml"))
        def upper(s): 
            return s.upper()
        td.set_on_globals("upper", upper)
        p = td.get_template('raw_nested.html#preferences')
        self.assertEqual(p.raw, True)
        self.assertEqual(p.qsclass, unistr)

    def test_prefer_with_overrides(self):
        td = Domain(DEFAULT_DIR, restricted=RESTRICTED, errors=ERRORS)
        def upper(s): 
            return s.upper()
        def trim(s): 
            return s.strip()
        td.set_on_globals("upper", upper)
        td.set_on_globals("trim", upper)
        p = td.get_template('raw_nested.html#preferences', raw=False, filters=[trim, upper])
        self.assertEqual(p.raw, False)
        self.assertEqual(p.qsclass, unistr)
        r = 'SHOULD REFRESH [QUOTING: NONE OR !="STR"] WHEN TEMPLATE IS LOADED'
        self.assertEqual(r, p.evoque())
        r = 'SHOULD REFRESH [QUOTING: NONE OR !="STR"] WHEN CHANGED TEMPLATE IS LOADED'
        self.assertEqual(r, p.evoque(what="changed template"))
    
    def test_filter_markdown(self):
        try:
            from markdown import markdown
        except ImportError:
            pr("Can't import markdown, skipping test [filter_markdown]")
            return
        td = Domain(DEFAULT_DIR, restricted=RESTRICTED, errors=ERRORS)
        td.set_on_globals("markdown", markdown)
        import logging
        logging.getLogger("MARKDOWN").setLevel(logging.INFO) # hide markdown DEBUG logging
        t = td.get_template('markdown.html')
        sub_out = "item two &lt;xml/&gt;"
        self.failIf(t.evoque().find(sub_out) == -1)
        # Test direct evoque'ation of inner my-markdown-template -- that should
        # now be already loaded with quoting="xml" --- with different quoting.
        # We retrieve it, and evoque it overriding the quoting (as well as 
        # supplying the needed param="<xml/>")
        m = td.get_template('markdown.html#my-markdown-template')
        self.failUnless(m.evoque(quoting="str", param="<xml/>"
                ).find(sub_out) == -1)
    
    def test_expr_formatting(self):
        td = Domain(DEFAULT_DIR, restricted=RESTRICTED, errors=ERRORS)
        data = dict(amount=1.0/3)
        src = "${amount!.4f}"
        td.set_template("t1", src=src, from_string=True)
        self.assertEqual("0.3333", td.get_template("t1").evoque(**data))
        src = "${ amount ! .3f }"
        td.set_template("t2", src=src, from_string=True)
        self.assertEqual("0.333", td.get_template("t2").evoque(**data))

    def test_alt_delimeters(self):
        td = Domain(DEFAULT_DIR, restricted=RESTRICTED, errors=ERRORS)
        t = td.get_template('for_seq_items.html')
        self.assertEqual(t.prefer.get("data").get("items")[0][0], "Apples")
    
    def test_mid_text(self):
        td = Domain(DEFAULT_DIR, restricted=RESTRICTED, errors=ERRORS)
        t = td.get_template('mid_text.html')
        subr = '</div><p class="middle">5</p><div width="100%">'
        self.failUnless(bool(t.evoque().index(subr)))

    def test_evoque_kwargs_raise_errors(self):
        td = Domain(DEFAULT_DIR, restricted=RESTRICTED, errors=4)
        t = td.get_template('evoque_kwargs.html')
        self.assertRaises((KeyError,), t.evoque, dyn_collection="ooops")
    
    def test_evoque_kwargs(self):
        td = Domain(DEFAULT_DIR, restricted=RESTRICTED, errors=4)
        r = "<h1>TITLE</h1><p>some PARAM text</p>"
        r_raw = "<h1>${title}</h1><p>some ${param} text</p>"
        r_q_str = "&lt;h1&gt;TITLE&lt;/h1&gt;&lt;p&gt;some PARAM text&lt;/p&gt;"
        responses = [ r, r, r, r, r, r_raw, r, r_q_str, r ]
        t = td.get_template('evoque_kwargs.html')
        for i, s in enumerate(t.test()):
            self.assertEqual(responses[i], s)
    
    def test_multi_labels(self):
        name = 'multi_labels.html'
        td = Domain(DEFAULT_DIR, restricted=RESTRICTED, errors=4)
        self.assertRaises((SyntaxError,), td.get_template, name)
    

if __name__ == '__main__':
    unittest.main()
    
