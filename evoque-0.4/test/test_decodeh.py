# -*- coding: utf-8 -*-
'''
Evoque - managed eval-based freeform templating 
Copyright (C) 2007 Mario Ruggier <mario@ruggier.org>
Licensed under the Academic Free License version 3.0
URL: http://evoque.gizmojo.org/
'''
__url__ = "$URL: svn://gizmojo.org/pub/evoque/trunk/test/test_decodeh.py $"
__revision__ = "$Id: test_decodeh.py 1143 2009-01-17 17:53:15Z mario $"

from os.path import abspath, join, dirname, splitext
import unittest
from evoque.decodeh import decode_from_file, decode_heuristically

import sys
def pr(*args):
    sys.stdout.write(" ".join([str(arg) for arg in args])+'\n')

#

def absname(name):
    return abspath(join(dirname(__file__), "data", name))

def write_binary_file(name, bytes):
    f = open(absname(name), "wb")
    f.write(bytes)
    f.close()

def read_binary_file(filename): # enc=None, encodings=ENCS, mdb=MDB, lossy=False
    return open(filename, 'rb').read()

#
# ensurce some non-ascii chars
# garçon très 
# 

# Python 3: An end to Unicode Problems?
# http://www.voidspace.org.uk/python/weblog/arch_d7_2008_12_06.shtml#e1041

class DecodehTest(unittest.TestCase):

    def test_utf8_file(self):
        filename = splitext(__file__)[0] + ".py"
        # decode by letting it read from file directly
        u1 = decode_from_file(filename)
        # second way by reading file as binary first, and then decoding the 
        # binary string
        b1 = read_binary_file(filename)
        u2_enc_lossy = decode_heuristically(b1)
        # assert that the two unicode strings are equal
        self.assertEqual(u1, u2_enc_lossy[0])
        # assert that enc="utf_8" and that decoding was not "lossy"
        self.assertEqual(u2_enc_lossy[2], False)
        self.assertEqual(u2_enc_lossy[1], "utf_8")

    def test_cp1252_file(self):
        # write file under py3.0 only
        #bs = b"some cp1252 \n \x80\x81\x82\x83\x84 \nchars"
        #write_binary_file(absname("dh_cp1252.txt"), bs)
        #
        u1 = decode_from_file(absname("dh_cp1252.txt"))
        u2_enc_lossy = decode_heuristically(
            read_binary_file(absname("dh_cp1252.txt")))
        self.assertEqual(u1, u2_enc_lossy[0])
        # The following i svery likely to give different results on differnet 
        # platforms:
        #pr("test_cp1252_file", u2_enc_lossy[1:])
        #self.failUnless(u2_enc_lossy[1] in ["cp1252", "mac-roman"] )
        self.assertEqual(u2_enc_lossy[2], False)


if __name__ == '__main__':
    unittest.main()
