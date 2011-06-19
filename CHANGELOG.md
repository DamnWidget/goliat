Goliat ChangeLog
================

This file isn't a real changelog, we use our code commits for details on technical changes.
This changelog file is a list of huge changes or bugfixes.

Version: 0.2.0 (In development):
--------------------------------

    * Twisted over Storm support removed. The twisted-integration brach will never be
      merged into the master Storm branch.
    * Added inotify support to the resources loader, now you can modify or add
      a new controller in runtime and goliat will reload it without restart the
      entire application.
    * Added HTML5 Doctype support.
    * Added OrderedDict() support for python 2.4, 2.5, 2.6 and 2.7

Version: 0.1.1 (Thu Apr 22 13:45:49 2010):
------------------------------------------

    * Added command line interface
    * Code refactorization for Python 3.0 future merge
    * Added the template system
    * Added JavaScript Goliat UI Applications Interface
    * Added INI settings manager
    * Added ExtJS 3.X support
    * Added Multi Service Manager
    * Added Goliat Crystal Theme
    * Added YAML schema files parser
    * Added Storm ORM support (with or without Twisted) 

Version: 0.1.0 (Sat Apr 3 02:48:11 2010):
-----------------------------------------

    * Initial relase
