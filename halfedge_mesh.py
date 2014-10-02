class HalfedgeMesh:
    def __init__(self, filename=None):
        """Make an empty halfedge mesh."""
        self.vertices = []
        self.halfedges = []
        self.facets = []

    def parse_off(self, filename):
        """Parses OFF files and returns a set of vertices, halfedges, and
        facets.
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
            pass

        def halfedges(self):
            """Return a list of halfedges targeting to this vertex."""
            pass

    class Facet:
        def __init__(self, index):
            """Create a facet with the given index."""
            pass

        def halfedges(self):
            """Return halfedges going ccw around this facet."""
            pass

    class Halfedge:
        def __init__(self, index):
            """Create a halfedge with given index."""
            pass
        def opposite(self):
            """Return the opposite halfedge."""
            pass

        def next(self):
            """Return the opposite halfedge."""
            pass

        def prev(self):
            """Return the opposite halfedge."""
            pass

        def vertex(self):
            """Return the target vertex."""
            pass

        def facet(self):
            """Return the incident facet."""
            pass


if __name__ == '__main__':
    m = HalfedgeMesh()
