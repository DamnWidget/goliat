Evoque - managed eval-based freeform templating 
Copyright (C) 2007 Mario Ruggier <mario at ruggier.org>
Licensed under the Academic Free License version 3.0
URL: http://evoque.gizmojo.org/
------------------------------------------------------------------------------
$URL: svn://gizmojo.org/pub/evoque/trunk/README.txt $
$Id: README.txt 1156 2009-01-20 12:18:24Z mario $
------------------------------------------------------------------------------

All DOCUMENTATION is at:

    http://evoque.gizmojo.org/ 

------------------------------------------------------------------------------
INSTALLATION

To install Evoque, you may use either easy_install or standard python 
distutils (i.e. download, unpack, install) as detailed below. 

$begin{installation}
# Installing with easy_install

easy_install evoque
easy_install qpy # optional, recommended

# Installing with distutils

wget http://gizmojo.org/dist/evoque-0.4.tar.gz 
tar zxvf evoque-0.4.tar.gz 
cd evoque-0.4
python setup.py install

cd .. # qpy, optional, recommended
wget http://www.mems-exchange.org/software/files/qpy/qpy-1.7.tar.gz
tar xzf qpy-1.7.tar.gz
cd qpy-1.7
python setup.py install

# Test

python evoque-0.4/test/test_evoque.py 
$end{installation}

------------------------------------------------------------------------------
