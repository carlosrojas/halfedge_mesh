#! /usr/bin/env python

try:
    from setuptools import setup, Command
except ImportError:
    from distutils.core import setup, Command

class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys,subprocess
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)

setup(
    name='halfedge_mesh',
    author_email="crojas@ucdavis.edu",
    description="Halfedge data structure for triangulated meshes",
    version='1.0',
    packages=['halfedge_mesh'],
    cmdclass={'test':PyTest}
)

