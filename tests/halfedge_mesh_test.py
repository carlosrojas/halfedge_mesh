import halfedge_mesh
import pytest
import math


class TestHalfedgeMesh:
    @pytest.fixture(scope="module")
    def cube_off_mesh(self):
        return halfedge_mesh.HalfedgeMesh("tests/data/cube.off", [213])

    def test_facet_test_halfedges_returns_all_halfedges(self, cube_off_mesh):
        halfedges = cube_off_mesh.facets[0].halfedges

        # Edge vertex 0 -> 1
        assert halfedges[0].vertex == halfedge_mesh.Vertex(1, -1, 1, 0)
        assert halfedges[0].prev.vertex == halfedge_mesh.Vertex(1, -1, -1,
                                                                0)

        # Edge vertex 1 -> 2
        assert halfedges[1].vertex == halfedge_mesh.Vertex(-1, -1, 1, 0)
        assert halfedges[1].prev.vertex == halfedge_mesh.Vertex(1, -1, 1, 0)

        # Edge vertex 2 -> 0
        assert halfedges[2].vertex == halfedge_mesh.Vertex(1, -1, -1, 0)
        assert halfedges[2].prev.vertex == halfedge_mesh.Vertex(-1, -1, 1, 0)

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

    def test_get_normals(self, cube_off_mesh):
        normals = cube_off_mesh.get_normals()
        import numpy as np

        assert np.allclose(np.array([0,-1,0]), np.asarray(normals[0]), atol=1e-6)
        assert np.allclose(np.array([0,1,0]), np.asarray(normals[1]), atol=1e-6)
        assert np.allclose(np.array([1,0,0]), np.asarray(normals[2]), atol=1e-6)
        assert np.allclose(np.array([0,0,1]), np.asarray(normals[3]), atol=1e-6)
        assert np.allclose(np.array([-1,0,0]), np.asarray(normals[4]), atol=1e-6)
        assert np.allclose(np.array([0,0,-1]), np.asarray(normals[5]), atol=1e-6)
        assert np.allclose(np.array([0,-1,0]), np.asarray(normals[6]), atol=1e-6)
        assert np.allclose(np.array([1,0,0]), np.asarray(normals[7]), atol=1e-6)
        assert np.allclose(np.array([0,0,-1]), np.asarray(normals[8]), atol=1e-6)
        assert np.allclose(np.array([0,1,0]), np.asarray(normals[9]), atol=1e-6)
        assert np.allclose(np.array([-1,0,0]), np.asarray(normals[10]), atol=1e-6)
        assert np.allclose(np.array([0,0,1]), np.asarray(normals[11]), atol=1e-6)

    def test_internal_norm(self):
        assert halfedge_mesh.halfedge_mesh.norm([0,-1,0]) == 1.0
        assert halfedge_mesh.halfedge_mesh.norm([0,1,0]) == 1.0
        assert halfedge_mesh.halfedge_mesh.norm([1,0,0]) == 1.0
        assert halfedge_mesh.halfedge_mesh.norm([0,0,1]) == 1.0
        assert halfedge_mesh.halfedge_mesh.norm([-1,0,0]) == 1.0
        assert halfedge_mesh.halfedge_mesh.norm([0,0,-1]) == 1.0
        assert halfedge_mesh.halfedge_mesh.norm([0,-1,0]) == 1.0
        assert halfedge_mesh.halfedge_mesh.norm([1,0,0]) == 1.0
        assert halfedge_mesh.halfedge_mesh.norm([0,0,-1]) == 1.0
        assert halfedge_mesh.halfedge_mesh.norm([0,1,0]) == 1.0
        assert halfedge_mesh.halfedge_mesh.norm([-1,0,0]) == 1.0
        assert halfedge_mesh.halfedge_mesh.norm([0,0,1]) == 1.0
        assert halfedge_mesh.halfedge_mesh.norm([1,1,1]) == math.sqrt(3)

    def test_internal_cross_product(self):
        v_i = [1,0,0]
        v_j = [0,1,0]
        v_k = [0,0,1]
        assert halfedge_mesh.halfedge_mesh.cross_product(v_i, v_i) == [0,0,0]
        assert halfedge_mesh.halfedge_mesh.cross_product(v_i, v_j) == v_k
        assert halfedge_mesh.halfedge_mesh.cross_product(v_j, v_k) == v_i
        assert halfedge_mesh.halfedge_mesh.cross_product(v_k, v_i) == v_j
        assert halfedge_mesh.halfedge_mesh.cross_product(v_j, v_i) == map(lambda x: -x, v_k)
        assert halfedge_mesh.halfedge_mesh.cross_product(v_i, v_k) == map(lambda x: -x, v_j)
        assert halfedge_mesh.halfedge_mesh.cross_product(v_k, v_j) == map(lambda x: -x, v_i)

