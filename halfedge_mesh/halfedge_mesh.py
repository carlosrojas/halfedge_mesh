import config

# TODO: Reorder functions
class HalfedgeMesh:
    def __init__(self, filename=None, vertices=[], halfedges=[], facets=[]):
        """Make an empty halfedge mesh."""

        self.vertices = vertices
        self.halfedges = halfedges
        self.facets = facets
        self.edges = None

        if filename:
            self.vertices, self.halfedges, self.facets, self.edges = self.read_file(filename)

    def __eq__(self, other):
        # TODO: Test
        return self.vertices == other.vertices and \
               self.halfedges == other.halfedges and \
               self.facets == other.facet

    def __hash__(self):
        return hash(self.vertices) ^ hash(self.halfedges) ^ hash(self.facets) ^ \
               hash((self.vertices, self.halfedges, self.facets))

    def read_file(self, filename):
        """Determine the type of file and use the appropriate parser.

        Returns a HalfedgeMesh
        """
        try:
            with open(filename, 'r') as file:

                first_line = file.readline().strip()

                # TODO: build OBJ, PLY parsers
                parser_dispatcher = {"OFF": self.parse_off(file),
                                     "PLY": None,
                                     "OBJ": None}

                return parser_dispatcher[first_line]

        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)

    def read_off_vertices(self, file_object, number_vertices):
        """Read each line of the file_object and return a list of Vertex types.
        The list will be as [V1, V2, ..., Vn] for n vertices

        Return a list of vertices.
        """
        vertices = []

        # Read all the vertices in
        for index in range(number_vertices):
            line = file_object.readline().split()

            # convert strings to floats
            line = map(float, line)
            vertices.append(Vertex(line[0], line[1], line[2], index))

        return vertices

    def parse_build_halfedge_off(self, file_object, number_facets, vertices):
        """Replicate:

        map< pair<unsigned int, unsigned int>, HalfEdge* > Edges;

        for each face F
        {
            for each edge (u,v) of F
            {
                Edges[ pair(u,v) ] = new HalfEdge();
                Edges[ pair(u,v) ]->face = F;
            }
            for each edge (u,v) of F
            {
                set Edges[ pair(u,v) ]->nextHalfEdge to next half-edge in F
                if ( Edges.find( pair(v,u) ) != Edges.end() )
                {
                    Edges[ pair(u,v) ]->oppositeHalfEdge = Edges[ pair(v,u) ];
                    Edges[ pair(v,u) ]->oppositeHalfEdge = Edges[ pair(u,v) ];
            }
        }

        """
        Edges = {}
        facets = []

        # For each facet
        for index in range(number_facets):
            line = file_object.readline().split()

            # convert strings to ints
            line = map(int, line)

            # TODO: make general to support non-triangular meshes
            # Facets vertices are in counter-clockwise order
            facet = Facet(line[1], line[2], line[3], index)
            facets.append(facet)

            # create pairing of vertices for example if the vertices are
            # verts = [1,2,3] then zip(verts, verts[1:]) = [(1,2),(2,3)]
            # note: we skip line[0] because it represents the number of vertices
            # in the facet.
            all_facet_edges = zip(line[1:], line[2:])
            all_facet_edges.append((line[3], line[1]))

            # For every (half)edge around the facet
            for i in range(3):
                Edges[all_facet_edges[i]] = Halfedge()
                Edges[all_facet_edges[i]].facet = facet
                Edges[all_facet_edges[i]].vertex = vertices[all_facet_edges[i][1]]

            facet.halfedges = [Edges[all_facet_edges[i]] for i in range(3)]

            for i in range(3):
                Edges[all_facet_edges[i]].next = Edges[all_facet_edges[(i + 1) % 3]]
                Edges[all_facet_edges[i]].prev = Edges[all_facet_edges[(i - 1) % 3]]

                # reverse edge ordering of vertex, e.g. (1,2)->(2,1)
                if all_facet_edges[i][2::-1] in Edges:
                    Edges[all_facet_edges[i]].opposite = \
                        Edges[all_facet_edges[i][2::-1]]

                    Edges[all_facet_edges[i][2::-1]].opposite = \
                        Edges[all_facet_edges[i]]

        return facets, Edges

    def parse_off(self, file_object):
        """Parses OFF files

        Returns a HalfedgeMesh
        """
        vertices = []
        halfedges = []
        facets = []

        vertices_faces_edges_counts = map(int, file_object.readline().split())

        number_vertices = vertices_faces_edges_counts[0]
        vertices = self.read_off_vertices(file_object, number_vertices)

        number_facets = vertices_faces_edges_counts[1]
        facets, Edges = self.parse_build_halfedge_off(file_object,
                                                      number_facets, vertices)

        for key, value in Edges.iteritems():
            halfedges.append(value)

        return vertices, halfedges, facets, Edges

    def get_halfedge(self, u, v):
        """Retrieve halfedge with starting vertex u and target vertex v

        u - starting vertex
        v - target vertex

        Returns a halfedge
        """
        return self.edges[(u,v)]



class Vertex:
    def __init__(self, x=0, y=0, z=0, index=None, halfedges=[]):
        """Create a vertex with given index at given point.

        x     - x-coordinate of the point
        y     - y-coordinate of the point
        z     - z-coordinate of the point
        index - integer index of this vertex
        halfedges = a list of halfedges targeting to this vertex.
        """

        self.x = x
        self.y = y
        self.z = z

        self.index = index
        self.halfedges = halfedges

    def __eq__(self, other):
        return (self.x - other.x) < config.EPSILON and \
               (self.y - other.y) < config.EPSILON and \
               (self.z - other.z) < config.EPSILON

    def __hash__(self):
        return hash(self.x) ^ hash(self.y) ^ hash(self.z) ^ hash(self.index) ^ \
               hash(self.halfedges) ^ \
               hash((self.x, self.y, self.z, self.index, self.halfedges))


class Facet:
    def __init__(self, a=-1, b=-1, c=-1, index=None, halfedges=[]):
        """Create a facet with the given index with three vertices.

        a, b, c - indices for the vertices in the facet, counter clockwise.
        index - index of facet in the mesh
        halfedges - a list of Halfedge types that belong to the facet
        """
        self.a = a
        self.b = b
        self.c = c
        self.index = index
        # halfedges going ccw around this facet.
        self.halfedges = halfedges

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b and self.c == other.c \
        and self.halfedges == other.halfedges


    def __hash__(self):
        return hash(self.halfedges) ^ hash(self.a) ^ hash(self.b) ^ \
               hash(self.c) ^ hash(self.index) ^ \
               hash((self.halfedges, self.a, self.b, self.c, self.index))


class Halfedge:
    def __init__(self, next=None, opposite=None, prev=None, vertex=None,
                 facet=None):
        """Create a halfedge with given index.
        """
        self.opposite = opposite
        self.next = next
        self.prev = prev
        self.vertex = vertex
        self.facet = facet

    def __eq__(self, other):
        return (self.vertex == other.vertex) and (self.facet == other.facet)

    def __hash__(self):
        return hash(self.opposite) ^ hash(self.next) ^ hash(self.prev) ^ \
               hash(self.vertex) ^ hash(self.facet) ^ hash((self.opposite,
                                                            self.next,
                                                            self.prev,
                                                            self.vertex,
                                                            self.facet))

