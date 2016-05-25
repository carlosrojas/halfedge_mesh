#! /usr/bin/env python

try:
    from setuptools import setup, Command
except ImportError:
    from distutils.core import setup, Command

setup(
    name='halfedge_mesh',
    author_email="crojas@ucdavis.edu",
    description="Halfedge data structure for triangulated meshes",
    version='1.0',
    packages=['halfedge_mesh'],
    setup_requires = ['pytest-runner'],
)

