import os
import tempfile                 # to make dummy path, not to make files

from nose.tools import eq_, raises
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


def check_is_valid_module_path(subdirs):
    assert isinstance(subdirs, list)
    rootpath = os.path.join(VALID_ABSPATH, 'root')
    abspath = os.path.join(rootpath, *subdirs)
    assert ImportFileMagic._is_valid_module_path(abspath, rootpath)


def test_is_valid_module_path():
    check_is_valid_module_path_fail = \
        raises(AssertionError)(check_is_valid_module_path)

    for subdirs in [['valid_module_name.py'],
                    ['valid_directory_name', 'module.py'],
                    ]:
        yield (check_is_valid_module_path, subdirs)

    for subdirs in [['invalid.directory.name', 'module.py']]:
        yield (check_is_valid_module_path_fail, subdirs)
