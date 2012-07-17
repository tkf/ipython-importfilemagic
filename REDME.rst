`%importfile` magic for IPython
===============================

`%importfile` tries to import Python file in most "natural way". For
example, if you have ``spam/egg/module.py``, ``spam/egg/__init__.py``
and ``spam/__init__.py``, you would want import ``module.py`` as
``spam.egg.module``, not as ``module`` or ``egg.module``.
`%importfile` tries several heuristics to find the best "module path".


Install::

  %install_ext https://raw.github.com/tkf/ipython-importfilemagic/master/importfilemagic.py

Usage::

  %importfile PATH/TO/SOME/FILE.py
