import config


class HalfedgeMesh:

    def __init__(self, filename = ""):
        """Make an empty halfedge mesh."""

        self.vertices = []
        self.halfedges = []
        self.facets = []

    def read_file(self, filename):
        """Determine the type of file and use the appropriate parser.

        filename - the file name, which might include the directory as well
        """
        pass

    @staticmethod
    def parse_off(self, file_object):
        """Parses OFF files

        Returns a set of vertices, halfedges, and facets.
        """
        pass

    def get_halfedge(self, u, v):
        """Retrieve halfedge with starting vertex u and target vertex v

        u - starting vertex
        v - target vertex

        Returns a halfedge
        """
        pass


class Vertex:

    def __init__(self, x, y, z, index):
        """Create a vertex with given index at given point.

        x     - x-coordinate of the point
        y     - y-coordinate of the point
        z     - z-coordinate of the point
        index - integer id of this vertex
        """

        self.x = x
        self.y = y
        self.z = z

        self.index = index

    def __eq__(self, other):
        return (self.x - other.x) < config.EPSILON and \
               (self.y - other.y) < config.EPSILON and \
               (self.z - other.z) < config.EPSILON

    def halfedges(self):
        """Return a list of halfedges targeting to this vertex.
        """
        pass


class Facet:

    def __init__(self, a, b, c, index):
        """Create a facet with the given index with three vertices.

        a, b, c - indices for the vertices in the facet, counter clockwise.
        index - index of facet in the mesh
        """
        self.a = a
        self.b = b
        self.c = c
        self.index = index

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b and self.c == other.c

    def halfedges(self):
        """Return halfedges going ccw around this facet.
        """
        pass


class Halfedge:

    def __init__(self, index):
        """Create a halfedge with given index.
        """
        pass

    def opposite(self):
        """Return the opposite halfedge.
        """
        pass

    def next(self):
        """Return the opposite halfedge.
        """
        pass

    def prev(self):
        """Return the opposite halfedge.
        """
        pass

    def vertex(self):
        """Return the target vertex.
        """
        pass

    def facet(self):
        """Return the incident facet.
        """
        pass
