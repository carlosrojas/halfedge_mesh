import halfedge_mesh
import pytest
import math


class TestHalfedgeMesh:

    @pytest.fixture(scope="module")
    def cube_off_mesh(self):
        return halfedge_mesh.HalfedgeMesh("tests/data/cube.off")

    def test_facet_halfedges_loops_facet(self, cube_off_mesh):
        halfedge = cube_off_mesh.facets[0].halfedge
        assert halfedge.next.next.next.vertex == halfedge.vertex

    def test_facet_halfedges_vertex_in_facet(self, cube_off_mesh):
        halfedge = cube_off_mesh.facets[0].halfedge

        vertices = set([halfedge_mesh.Vertex(1.0, -1.0, 1.0, 1),
                    halfedge_mesh.Vertex(1.0, -1.0, -1.0, 0),
                    halfedge_mesh.Vertex(-1.0, -1.0, 1.0, 2)])


        # make sure all vertices are in the facet described by halfedge
        assert halfedge.vertex in vertices
        vertices.remove( halfedge.vertex )

        assert halfedge.next.vertex in vertices
        vertices.discard( halfedge.next.vertex)

        assert halfedge.next.next.vertex in vertices
        vertices.discard( halfedge.next.next.vertex)

    def test_facet_eq_correct_for_same_object_and_diff_objects(self,
                                                               cube_off_mesh):
        assert cube_off_mesh.facets[0] == cube_off_mesh.facets[0]
        assert cube_off_mesh.facets[1] != cube_off_mesh.facets[0]

        assert cube_off_mesh.facets[3] == cube_off_mesh.facets[3]
        assert cube_off_mesh.facets[0] != cube_off_mesh.facets[3]

    def test_halfedgemesh_vertices_are_in_order_with_cubeoff(self,
                                                             cube_off_mesh):
        # Tests parse_off since Vertex is just a basic class
        vertices = cube_off_mesh.vertices

        # cube vertices in order
        pts = [1, -1, -1,
               1, -1, 1,
               -1, -1, 1,
               -1, -1, -1,
               1, 1, -0.999999,
               0.999999, 1, 1.000001]

        count = 0
        for index in range(0, len(vertices), 3):
            # Vertex(a,b,c, index)
            assert vertices[count] == halfedge_mesh.Vertex(pts[index],
                                                           pts[index + 1],
                                                           pts[index + 2], count)
            count += 1

    def test_halfedgemesh_vertices_in_facet_exists_with_cubeoff(self,
                                                                cube_off_mesh):
        # Tests parse_off since Vertex is just a basic class

        facets = cube_off_mesh.facets
        vertices = cube_off_mesh.vertices

        for index in range(len(facets)):
            # check that it's within the range of the number of vertices
            assert facets[index].a < len(vertices)
            assert (facets[index].a >= 0)

    def test_halfedgemesh_get_halfedge_returns_correct_vertices_with_cubeoff(
            self, cube_off_mesh):

        five_seven = cube_off_mesh.get_halfedge(5, 7)
        assert five_seven.vertex.index == 7
        assert five_seven.prev.vertex.index == 5

        five_six = cube_off_mesh.get_halfedge(5, 6)
        assert five_six.vertex.index == 6
        assert five_six.prev.vertex.index == 5

        one_two = cube_off_mesh.get_halfedge(1, 2)
        assert one_two.vertex.index == 2
        assert one_two.prev.vertex.index == 1

    def test_halfedge_opposite_correct_vertices_with_cubeoff(self,
                                                             cube_off_mesh):

        zero_two = cube_off_mesh.get_halfedge(0, 2)
        assert zero_two.opposite.vertex.index == 0
        assert zero_two.opposite.prev.vertex.index == 2

        zero_one = cube_off_mesh.get_halfedge(0, 1)
        assert zero_one.opposite.vertex.index == 0
        assert zero_one.opposite.prev.vertex.index == 1

        four_one = cube_off_mesh.get_halfedge(4, 1)
        assert four_one.opposite.vertex.index == 4
        assert four_one.opposite.prev.vertex.index == 1

    def test_halfedge_eq_correct_for_same_and_object_and_diff_objects(self,
                                                                      cube_off_mesh):

        zero_two = cube_off_mesh.get_halfedge(0, 2)
        assert zero_two == zero_two

        four_one = cube_off_mesh.get_halfedge(4, 1)
        assert zero_two != four_one

    def test_get_angle_normal(self, cube_off_mesh):
        assert cube_off_mesh.facets[0].halfedge.vertex.index == 1
        assert cube_off_mesh.facets[0].halfedge.prev.vertex.index == 0
        assert halfedge_mesh.allclose(
                cube_off_mesh.facets[0].halfedge.get_angle_normal(),
                math.pi/2.0)
    
        assert cube_off_mesh.facets[1].halfedge.vertex.index == 7
        assert cube_off_mesh.facets[1].halfedge.prev.vertex.index  == 4
        assert halfedge_mesh.allclose(
                cube_off_mesh.facets[1].halfedge.get_angle_normal(),
                math.pi/2.0)

        assert cube_off_mesh.facets[3].halfedge.next.vertex.index == 2
        assert cube_off_mesh.facets[3].halfedge.next.prev.vertex.index == 5
        assert halfedge_mesh.allclose(
                cube_off_mesh.facets[3].halfedge.next.get_angle_normal(), 0.0)

    def test_get_vertex(self, cube_off_mesh):
        mesh_vertex = cube_off_mesh.vertices[0].get_vertex() 
        test_vertex = halfedge_mesh.Vertex(1,-1,-1,0).get_vertex()
        assert halfedge_mesh.allclose(mesh_vertex,test_vertex)
                

def test_internal_norm():
    assert halfedge_mesh.norm([0, -1, 0]) == 1.0
    assert halfedge_mesh.norm([0, 1, 0]) == 1.0
    assert halfedge_mesh.norm([1, 0, 0]) == 1.0
    assert halfedge_mesh.norm([0, 0, 1]) == 1.0
    assert halfedge_mesh.norm([-1, 0, 0]) == 1.0
    assert halfedge_mesh.norm([0, 0, -1]) == 1.0
    assert halfedge_mesh.norm([0, -1, 0]) == 1.0
    assert halfedge_mesh.norm([1, 0, 0]) == 1.0
    assert halfedge_mesh.norm([0, 0, -1]) == 1.0
    assert halfedge_mesh.norm([0, 1, 0]) == 1.0
    assert halfedge_mesh.norm([-1, 0, 0]) == 1.0
    assert halfedge_mesh.norm([0, 0, 1]) == 1.0
    assert halfedge_mesh.norm([1, 1, 1]) == math.sqrt(3)


def test_internal_cross_product():
    v_i = [1, 0, 0]
    v_j = [0, 1, 0]
    v_k = [0, 0, 1]
    assert halfedge_mesh.cross_product(v_i, v_i) == [0, 0, 0]
    assert halfedge_mesh.cross_product(v_i, v_j) == v_k
    assert halfedge_mesh.cross_product(v_j, v_k) == v_i
    assert halfedge_mesh.cross_product(v_k, v_i) == v_j
    assert halfedge_mesh.cross_product(v_j, v_i) == map(lambda x: -x, v_k)
    assert halfedge_mesh.cross_product(v_i, v_k) == map(lambda x: -x, v_j)
    assert halfedge_mesh.cross_product(v_k, v_j) == map(lambda x: -x, v_i)


def test_allclose_list_int_float():
    assert halfedge_mesh.allclose(1, 1)
    assert halfedge_mesh.allclose(0, 0)
    assert halfedge_mesh.allclose(-1, -1)
    assert halfedge_mesh.allclose([1.34, 1.4, 5688.66], [1.34, 1.4, 5688.66])
    assert halfedge_mesh.allclose(
        [-1.34, -1.4, -5688.66], [-1.34, -1.4, -5688.66])
    assert halfedge_mesh.allclose([1.33], [1.33])
    assert halfedge_mesh.allclose(1.33, 1.33)
    assert halfedge_mesh.allclose([1, 2, 3, 4], [1, 2, 3, 4])
    assert halfedge_mesh.allclose([-1, -2, -3, -4], [-1, -2, -3, -4])


def test_dot():
    assert halfedge_mesh.dot([1, 2, 3], [1, 2, 3]) == 14
    assert halfedge_mesh.dot([-1, -2, -3], [1, 2, 3]) == -14
    assert halfedge_mesh.dot([1, 2, 3], [-1, -2, -3]) == -14
    assert halfedge_mesh.dot([0, 1, 0], [1, 0, 0]) == 0
    assert halfedge_mesh.dot([0, -1, 0], [-1, 0, 0]) == 0
    assert halfedge_mesh.dot([1, 0, 0], [0, 0, 1]) == 0
    assert halfedge_mesh.dot([1], [2]) == 2
    assert halfedge_mesh.dot([3, 4], [10, 8]) == 62
    assert halfedge_mesh.allclose((halfedge_mesh.dot([1.23, 4.5, 0.0],
                                                     [1.3865, 4.56, 81.3865])),
                                                     22.225394999999999)


def test_make_iterable():
    assert halfedge_mesh.make_iterable([1]) == [1]
    assert halfedge_mesh.make_iterable([-1]) == [-1]
    assert halfedge_mesh.make_iterable(2) == [2]
    assert halfedge_mesh.make_iterable(-2) == [-2]
    assert halfedge_mesh.make_iterable((3)) == [3]
    assert halfedge_mesh.make_iterable((-3)) == [-3]
    assert halfedge_mesh.make_iterable((3, 2, 1)) == (3, 2, 1)
    assert halfedge_mesh.make_iterable((-3, -2, -1)) == (-3, -2, -1)
    assert halfedge_mesh.make_iterable(1.2345) == [1.2345]
    assert halfedge_mesh.make_iterable(-1.2345) == [-1.2345]
    assert halfedge_mesh.make_iterable([1.234, 344.33]) == [1.234, 344.33]


def test_normalize_vectors():
    assert halfedge_mesh.allclose(halfedge_mesh.normalize([1, 2, 3]),
                                  [0.26726124,  0.53452248,  0.80178373])

    assert halfedge_mesh.allclose(halfedge_mesh.normalize([3.43, 566.7, 9.6]),
                                  [0.00605161,  0.99983824,  0.01693744])

    assert halfedge_mesh.allclose(
        halfedge_mesh.normalize([100000., 1222222., 30000000]),
        [0.00333055,  0.04070674,  0.99916559])

    assert halfedge_mesh.allclose(halfedge_mesh.normalize([0,0,0]), [0,0,0])

def test_create_vector():
    p1 = [0,0,0]
    p2 = [-1,-1,-1]
    v = halfedge_mesh.create_vector(p1, p2)
    assert halfedge_mesh.allclose(v, [-1,-1,-1])

    p3 = [4,4,4]
    v = halfedge_mesh.create_vector(p2, p3)
    assert halfedge_mesh.allclose(v, [5,5,5])
