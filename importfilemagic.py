import os
import sys

from IPython.core.magic import Magics, magics_class, line_magic
from IPython.core.magic_arguments import (argument, magic_arguments,
                                          parse_argstring)
from IPython.utils.syspathcontext import prepended_to_syspath


@magics_class
class ImportFileMagic(Magics):

    @magic_arguments()
    @argument('path', help='a file path to be imported.')
    @argument('--reload', '-r', default=False, action='store_true',
              help='reload module')
    @argument('--star', '-s', default=False, action='store_true',
              help='do "from modeule import *"')
    @line_magic
    def importfile(self, parameter_s=''):
        """
        Import module given a file.

        This command tries to import a given file as a module.
        Following methods are applied in order:

        1. If the absolute path of a given file starts with one of the
           path in `sys.path`, the given file is imported as a normal
           module.
        2. If there is ``__init__.py`` is in each sub-directory from
           the current working directory and to the file, the given
           file is imported as a normal module.
        3. If there is `setup.py` in one of the parent directory of
           the given file, the file is imported as a module in a
           package located at the location where `setup.py` is.
        4. If none of above matches, the file is imported as a stand
           alone module.

        """
        args = parse_argstring(self.importfile, parameter_s)
        abspath = os.path.abspath(os.path.expanduser(args.path))

        for method in [self._method_sys_path,
                       self._method_init,
                       self._method_setup_py,
                       self._method_stand_alone]:
            rootpath = method(abspath)
            if rootpath:
                break

        modulepath = '.'.join(
            os.path.relpath(os.path.splitext(abspath)[0], rootpath)
            .split(os.path.sep))
        commands = ["import {0}".format(modulepath)]
        if args.reload:
            commands.append("reload({0})".format(modulepath))
        if args.star:
            commands.append("from {0} import *".format(modulepath))
        code = "\n".join(commands)
        print code

        with prepended_to_syspath(rootpath):
            self.shell.ex(code)

    @staticmethod
    def _method_sys_path(abspath):
        matches = []
        for p in filter(lambda x: x, sys.path):
            if abspath.startswith(p):
                matches.append(p)
        if matches:
            return sorted(matches)[-1]  # longest match

    @staticmethod
    def _method_init(abspath):
        cwd = os.getcwd()
        if not abspath.startswith(cwd):
            return
        subdirs = os.path.relpath(abspath, cwd).split(os.path.sep)
        while subdirs:
            if not os.path.exists(
                    os.path.join(os.path.join(cwd, *subdirs), '__init__.py')):
                return
            subdirs.pop()
        return cwd

    @staticmethod
    def _method_setup_py(abspath):
        dirs = abspath.split(os.path.sep)
        while len(dirs) > 1:
            dirs.pop()
            rootpath = os.path.sep.join(dirs)
            if os.path.exists(os.path.join(rootpath, 'setup.py')):
                return rootpath

    _method_stand_alone = staticmethod(os.path.dirname)


def load_ipython_extension(ip):
    """Load the extension in IPython."""
    global _loaded
    if not _loaded:
        ip.register_magics(ImportFileMagic)
        _loaded = True

_loaded = False
