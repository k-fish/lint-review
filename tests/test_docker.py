from __future__ import absolute_import
import lintreview.docker as docker
from nose.tools import eq_, assert_in
from tests import requires_image, test_dir


def test_replace_basedir():
    files = ['/tmp/things/some/thing.py', 'some/other.py']
    out = docker.replace_basedir('/tmp/things', files)
    expected = ['/src/some/thing.py', '/src/some/other.py']
    eq_(expected, out)


def test_strip_base():
    eq_('some/thing.py', docker.strip_base('/src/some/thing.py'))
    eq_('some/thing.py', docker.strip_base('some/thing.py'))
    eq_('some/src/thing.py', docker.strip_base('some/src/thing.py'))


def test_apply_base():
    eq_('/src', docker.apply_base(''))
    eq_('/src', docker.apply_base('/'))
    eq_('/src/thing.py', docker.apply_base('thing.py'))
    eq_('/src/some/thing.py', docker.apply_base('some/thing.py'))
    eq_('thing.py', docker.apply_base('/some/thing.py'))
    eq_('thing.py', docker.apply_base('/some/../../thing.py'))


@requires_image('python2')
def test_run__unicode():
    cmd = ['echo', u"\u2620"]
    output = docker.run('python2', cmd, test_dir)
    eq_(output, u"\u2620\n")


@requires_image('python2')
def test_run__named_container():
    cmd = ['echo', "things"]
    docker.run('python2', cmd, test_dir, name='test_container')
    containers = docker.containers(include_stopped=True)
    assert_in('test_container', containers)
    docker.rm_container('test_container')

    containers = docker.containers(include_stopped=True)
    assert 'test_conainer' not in containers


@requires_image('python2')
def test_images():
    result = docker.images()
    assert_in('python2', result)
