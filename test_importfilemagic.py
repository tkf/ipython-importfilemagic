import os
import tempfile                 # to make dummy path, not to make files

from nose.tools import eq_
import mock

from importfilemagic import ImportFileMagic

VALID_ABSPATH = tempfile.gettempdir()


def test_has_init():
    rootpath = os.path.join(VALID_ABSPATH, 'root')
    abspath = os.path.join(rootpath, 'a', 'b', 'c.py')
    exists = mock.Mock(return_value=True)
    with mock.patch('os.path.exists', exists):
        assert ImportFileMagic._has_init(abspath, rootpath)

    exists.assert_any_call(os.path.join(rootpath, 'a', 'b', '__init__.py'))
    exists.assert_any_call(os.path.join(rootpath, 'a', '__init__.py'))
    eq_(exists.call_count, 2)
