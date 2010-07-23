Evoque - managed eval-based freeform templating 
Copyright (C) 2007 Mario Ruggier <mario at ruggier.org>
Licensed under the Academic Free License version 3.0
URL: http://evoque.gizmojo.org/
------------------------------------------------------------------------------
$URL: svn://gizmojo.org/pub/evoque/trunk/bench/README.txt $
$Id: README.txt 1034 2008-07-27 08:21:57Z mario $
------------------------------------------------------------------------------

Templating benchmarks folder. 

To run these benchmaks for all templating systems, please do:

    cd <evoque-dist-folder>/bench
    python subs.py 
    python basic.py 
    python bigtable.py 

However this will generate errors if any templating system being benchmarked
is not installed. To run for only specific templating systems, please specify
the system as a command line parameter, for example:

    python subs.py  pystr_nq qpy evoque evoque_mq evoque_r mako mako_mq genshi_text_mq
    python basic.py          qpy evoque evoque_mq evoque_r mako mako_mq genshi
    python bigtable.py       qpy evoque evoque_mq evoque_r mako mako_mq genshi

Note that running with -v will output also a sample of what is being generated, e.g:

    python basic.py -v  qpy evoque mako genshi

------------------------------------------------------------------------------
