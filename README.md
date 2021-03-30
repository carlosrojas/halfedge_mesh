# Halfedge Mesh
This is a small python library that will read OFF mesh format files into
a halfedge data structure. A halfedge data structure has two edges for a given
edge in a mesh.

## Usage

Here I run through some basic manipulations of a mesh.

    import halfedge_mesh

    # .off are supported
    mesh = halfedge_mesh("my_meshes.off")

    # Returns a list of Vertex type (in order of file)--similarly for halfedges,
    # and facets
    mesh.vertices

    # The number of facets in the mesh
    len(mesh.facets)

    # Get the 10th halfedge
    mesh.halfedges[10]

    # Get the halfedge that starts at vertex 25 and ends at vertex 50
    mesh.get_halfedge(25, 50)

Please refer to the documentation for more functionality.

## Test

### Option 1
Simply run

    python setup.py test

If you would like to see the coverage of the unit tests run

    python setup.py test --addopts --cov=halfedge_mesh

Note: this will not work with python 2.6 due to argparse dependency.

### Option 2
In order to run the tests in this project you must have py.test. To install
py.test you can either

    pip install -U pytest # or
    easy_install -U pytest

then you can simply run py.test in the home project directory. Make sure
halfedge_mesh is importable, for example by typing once:

    pip install -e .   # install package using setup.py in editable mode

## Help
Email me, Carlos Rojas at <carlos.rojas@sjsu.edu>

## Contribution Guidelines
Please follow the [PEP 8 style guide for python](http://legacy.python.org/dev/peps/pep-0008/)
and the [writing good commit guideline](https://github.com/erlang/otp/wiki/Writing-good-commit-messages)

Here are some helpful articles [git commits](http://ablogaboutcode.com/2011/03/23/proper-git-commit-messages-and-an-elegant-git-history/),
and [clean git history](https://www.reviewboard.org/docs/codebase/dev/git/clean-commits/).

## License
Halfedge Mesh is released under the MIT License.
