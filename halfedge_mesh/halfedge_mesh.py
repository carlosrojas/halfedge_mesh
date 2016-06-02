import sys
import config
import math


# TODO: Reorder functions
class HalfedgeMesh:

    def __init__(self, filename=None):
        """Make an empty halfedge mesh.

           filename   - a string that holds the directory location and name of
               the mesh
            vertices  - a list of Vertex types
            halfedges - a list of HalfEdge types
            facets    - a list of Facet types
        """
        self.vertex_list = []
        self.halfedge_list = []
        self.facet_list = []
        self.filename = filename

        if filename:
            self.vertex_list, self.halfedge_list, self.facet_list = self.read_file(filename)

    def __eq__(self, other):
        return (isinstance(other, type(self)) and self.__key() == other.__key())

    def __key(self):
        return (self.vertex_list, self.halfedge_list, self.halfedge_list, 
                self.filename)

    def __hash__(self):
        return hash(str(self.vertex_list)) ^ hash(str(self.halfedge_list)) ^ \
               hash(str(self.facet_list)) ^ hash(self.filename) ^ \
               hash(str(self.__key()))

    def discard_comments(self, file_object, current_token):
        comment_character = "#"

        while current_token == comment_character:
            current_token = file_object.readline().split()[0].upper()

        return current_token

    def read_file(self, filename):
        """Determine the type of file and use the appropriate parser. Currently,
        only support .OFF files.

        Returns a vertices, halfedges, facets
        """
        try:
            with open(filename, 'r') as file:

                # TODO Make ability to discard # lines
                first_line = file.readline().split()[0].upper()

                if first_line == "#":
                    first_line = self.discard_comments(file, first_line)

                if first_line != "OFF":
                    raise ValueError("Filetype: " + first_line + " not accepted")

                # TODO: build OBJ, PLY parsers
                parser_dispatcher = {"OFF": self.parse_off}
                                      
                return parser_dispatcher[first_line](file)

        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            return
        except ValueError as e:
            print "Value error: {0}:".format(e)
            return

    def parse_off(self, file_object):
        """Parses .OFF file

        Returns a vertices, halfedges, facets
        """
        facets, halfedges, vertices = [], [], []

        vertices_faces_edges_counts = map(int, file_object.readline().split())

        number_vertices = vertices_faces_edges_counts[0]
        vertices = self.read_off_vertices(file_object, number_vertices)

        number_facets = vertices_faces_edges_counts[1]
        facets, halfedges = self.parse_build_halfedge_off(file_object,
                                                      number_facets, vertices)
        return vertices, halfedges, facets

    def read_off_vertices(self, file_object, number_vertices):
        """Read each line of the file_object and return a list of Vertex types.
        The list will be as [V1, V2, ..., Vn] for n vertices

        Return a list of vertices.
        """
        vertices = []

        # Read all the vertices in
        for index in xrange(number_vertices):
            line = file_object.readline().split()

            try:
                # convert strings to floats
                line = map(float, line)
            except ValueError as e:
                raise ValueError("vertices " + str(e))

            vertices.append(Vertex(line[0], line[1], line[2], index, self))

        return vertices

    def parse_build_halfedge_off(self, file_object, number_facets, vertices):
        """Link to the code:
        http://stackoverflow.com/questions/15365471/initializing-half-edge-
        data-structure-from-vertices

        Pseudo code:
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
        edges = {}
        facets = []
        halfedges = []
        halfedge_count = 0

        #TODO Check if vertex index out of bounds
        # For each facet
        for index in xrange(number_facets):
            line = file_object.readline().split()

            # convert strings to ints
            line = map(int, line)

            # TODO: make general to support non-triangular meshes
            # facets vertices are in counter-clockwise order
            facet = Facet(line[1], line[2], line[3], index, self)
            facets.append(facet)

            # create pairing of vertices for example if the vertices are
            # verts = [1,2,3] then zip(verts, verts[1:]) = [(1,2),(2,3)]
            # note: we skip line[0] because it represents the number of vertices
            # in the facet. add (3,1) at the end.
            facet_edges = zip(line[1:], line[2:]) + [(line[3], line[1])]

            # For every halfedge around the facet
            for i in xrange(3):
                current_halfedge = Halfedge()
                current_halfedge.mesh = self
                current_halfedge.facet_id = facet.index

                current_halfedge.vertex_id = vertices[facet_edges[i][1]].index
                vertices[facet_edges[i][1]].halfedge_id = halfedge_count

                current_halfedge.index = halfedge_count

                halfedges.append(current_halfedge)

                edges[facet_edges[i]] = current_halfedge

                halfedge_count +=1

            facet.halfedge_id = edges[facet_edges[0]].index

            for i in xrange(3):
                edges[facet_edges[i]].next_id = edges[facet_edges[(i + 1) % 3]].index
                edges[facet_edges[i]].prev_id = edges[facet_edges[(i - 1) % 3]].index

                # reverse edge ordering of vertex, e.g. (1,2)->(2,1)
                if facet_edges[i][2::-1] in edges:
                    edges[facet_edges[i]].opposite_id = edges[facet_edges[i][2::-1]].index

                    edges[facet_edges[i][2::-1]].opposite_id = edges[facet_edges[i]].index

        return facets, halfedges

        
    def update_vertices(self, vertices):
        # update vertices
        for i, v in enumerate(vertices):
            self.vertex_list[i].x = v[0]
            self.vertex_list[i].y = v[1]
            self.vertex_list[i].z = v[2]

class Vertex:

    def __init__(self, x=0, y=0, z=0, index=None, mesh=None, halfedge_id=None):
        """Create a vertex with given index at given point.

        x           - x-coordinate of the point
        y           - y-coordinate of the point
        z           - z-coordinate of the point
        index       - integer index of this vertex
        halfedge_id - a halfedge index
        """

        self.x = x
        self.y = y
        self.z = z

        self.index = index

        self.mesh = mesh

        self.halfedge_id = halfedge_id

    def __eq__(self, other):
        return (allclose(self.__key(), other.__key()) and 
                isinstance(other, type(self)))

    def __key(self):
        return (self.x, self.y, self.z, self.index, self.halfedge_id)

    def __hash__(self):
        return hash(self.__key())

    def halfedge(self):
        return self.mesh.halfedge_list[self.halfedge_id]

    def coordinates(self):
        return [self.x, self.y, self.z]


class Facet:

    def __init__(self, a=-1, b=-1, c=-1, index=None, mesh=None, halfedge_id=None):
        """Create a facet with the given index with three vertices.

        a, b, c - indices for the vertices in the facet, counter clockwise.
        index - index of facet in the mesh
        halfedge - a Halfedge that belongs to the facet (index)
        """
        self.a = a
        self.b = b
        self.c = c
        self.index = index

        self.mesh = mesh

        # halfedge going ccw around this facet.
        self.halfedge_id = halfedge_id

    def __eq__(self, other):
        return (isinstance(other, type(self)) and self.__key() == other.__key())

    def __key(self):
        return (self.a, self.b, self.c, self.index, self.mesh, self.halfedge_id)

    def __hash__(self):
        return hash(self.a) ^ hash(self.b) ^ hash(self.c) ^ hash(self.index) ^\
               hash(self.mesh) ^ hash(self.halfedge_id) ^ hash(self.__key())

    def halfedge(self):
        return self.mesh.halfedge_list[self.halfedge_id]

    def normal(self):
        """Calculate the normal of facet

        Return a python list that contains the normal
        """
        vertex_a = self.halfedge().vertex().coordinates()

        vertex_b = self.halfedge().next().vertex().coordinates()

        vertex_c = self.halfedge().prev().vertex().coordinates()
        
        # create edge 1 with vector difference
        edge1 = [u - v for u, v in zip(vertex_b, vertex_a)]
        edge1 = normalize(edge1)
        # create edge 2 ...
        edge2 = [u - v for u, v in zip(vertex_c, vertex_b)]
        edge2 = normalize(edge2)

        # cross product
        normal = cross_product(edge1, edge2)

        normal = normalize(normal)

        return normal

class Halfedge:

    def __init__(self, opposite_id=None, next_id=None, prev_id=None, 
                 vertex_id=None, facet_id=None, index=None, mesh=None):
        """Create a halfedge with given index.
        """
        self.opposite_id = opposite_id
        self.next_id = next_id
        self.prev_id = prev_id
        self.vertex_id = vertex_id 
        self.facet_id = facet_id
        self.index = index
        self.mesh = mesh

    def __eq__(self, other):
        return (isinstance(other, type(self)) and self.__key() == other.__key())

    def __key(self):
        return (self.opposite_id, self.next_id, self.prev_id, self.vertex_id,
                self.facet_id, self.index, self.mesh)

    def __hash__(self):
        return hash(self.opposite_id) ^ hash(self.next_id) ^ \
               hash(self.prev_id) ^ hash(self.vertex_id) ^ \
               hash(self.facet_id) ^ hash(self.index) ^ hash(self.mesh) ^ \
               hash(self.__key())

    def opposite(self):
        return self.mesh.halfedge_list[self.opposite_id]

    def next(self):
        return self.mesh.halfedge_list[self.next_id]

    def prev(self):
        return self.mesh.halfedge_list[self.prev_id]

    def vertex(self):
        return self.mesh.vertex_list[self.vertex_id]

    def facet(self):
        return self.mesh.facet_list[self.facet_id]

    def angle_normal(self):
        """Calculate the angle between the normals that neighbor the edge.

        Return an angle in radians
        """
        a = self.facet().normal()
        b = self.opposite().facet().normal()

        dir = map(lambda x,y: x-y, self.vertex().coordinates(), self.prev().vertex().coordinates())
        
        dir = normalize(dir)

        ab = dot(a, b)

        args = ab / (norm(a) * norm(b))

        if allclose(args, 1):
            args = 1
        elif allclose(args, -1):
            args = -1

        assert (args <= 1.0 and args >= -1.0)

        angle = math.acos(args)
        #print angle, a, b

        if not (angle % math.pi == 0):
            e = cross_product(a, b)
            e = normalize(e)

            vec = dir
            vec = normalize(vec)

            if (allclose(vec, e)):
                return angle
            else:
                return -angle
        else:
            return 0

def allclose(v1, v2):
    """Compare if v1 and v2 are close

    v1, v2 - any numerical type or list/tuple of numerical types

    Return bool if vectors are close, up to some epsilon specified in config.py
    """

    v1 = make_iterable(v1)
    v2 = make_iterable(v2)

    elementwise_compare = map(
        (lambda x, y: abs(x - y) < config.EPSILON), v1, v2)
    return reduce((lambda x, y: x and y), elementwise_compare)


def make_iterable(obj):
    """Check if obj is iterable, if not return an iterable with obj inside it.
    Otherwise just return obj.

    obj - any type

    Return an iterable
    """
    try:
        iter(obj)
    except:
        return [obj]
    else:
        return obj


def dot(v1, v2):
    """Dot product(inner product) of v1 and v2

    v1, v2 - python list

    Return v1 dot v2
    """
    elementwise_multiply = map((lambda x, y: x * y), v1, v2)
    return reduce((lambda x, y: x + y), elementwise_multiply)


def norm(vec):
    """ Return the Euclidean norm of a 3d vector.

    vec - a 3d vector expressed as a list of 3 floats.
    """
    return math.sqrt(reduce((lambda x, y: x + y * y), vec, 0.0))


def normalize(vec):
    """Normalize a vector

    vec - python list

    Return normalized vector
    """
    if norm(vec) < 1e-6:
        return [0 for i in xrange(len(vec))]
    return map(lambda x: x / norm(vec), vec)


def cross_product(v1, v2):
    """ Return the cross product of v1, v2.

    v1, v2 - 3d vector expressed as a list of 3 floats.
    """
    x3 = v1[1] * v2[2] - v2[1] * v1[2]
    y3 = -(v1[0] * v2[2] - v2[0] * v1[2])
    z3 = v1[0] * v2[1] - v2[0] * v1[1]
    return [x3, y3, z3]


def create_vector(p1, p2):
    """Contruct a vector going from p1 to p2.

    p1, p2 - python list wth coordinates [x,y,z].

    Return a list [x,y,z] for the coordinates of vector
    """
    return map((lambda x,y: x-y), p2, p1)
