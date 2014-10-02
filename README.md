#Halfedge Mesh
This is a small python library that will read OBJ and PLY mesh format files into
a halfedge data structure. A halfedge data structure has two edges for a given
edge in a mesh.

##Usage

Here I run through some basic manipulations of a mesh.

    import halfedge_mesh
    
    # Either .off or .py are supported
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

##Help
Email me, Carlos Rojas at <iam@carlosrojas.me>

##Contribution Guidelines
Please follow the [PEP 8 style guide for python](http://legacy.python.org/dev/peps/pep-0008/)
and the [writing good commit guideline](https://github.com/erlang/otp/wiki/Writing-good-commit-messages)

##License
Halfedge Mesh is released under the MIT License.

##Credits