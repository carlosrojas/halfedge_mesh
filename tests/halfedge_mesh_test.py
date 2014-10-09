import halfedge_mesh
import pytest


class TestHalfedgeMesh:
    @pytest.fixture()
    def cube_off_mesh(self, scope="module"):
        return halfedge_mesh.HalfedgeMesh("test_data/cube.off")

    def test_halfedgemesh_vertices_are_in_order_with_cubeoff(self,
                                                             cube_off_mesh):
        # Tests parse_off since Vertex is just a basic class
        vertices = cube_off_mesh.vertices

        # cube vertices in order
        pts = [8, 12, 18, 1, -1, -1, 1, -1, 1, -1, -1, 1, -1, -1, -1, 1, 1,
               -0.999999, 0.999999, 1, 1.000001]

        for index in range(0, len(vertices), 3):
            # Vertex(a,b,c, id) id doesn't matter so it is set to zero
            assert vertices[index] == halfedge_mesh.Vertex(pts[index],
                                                           pts[index + 1],
                                                           pts[index + 2], 0)

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
        assert five_seven.vertex().id == 7
        assert five_seven.prev().vertex().id == 5

        five_six = cube_off_mesh.get_halfedge(5, 6)
        assert five_six.vertex().id == 6
        assert five_six.prev().vertex().id == 5

        one_two = cube_off_mesh.get_halfedge(1, 2)
        assert one_two.vertex().id == 1
        assert one_two.prev().id == 2

    def test_halfedge_opposite_correct_vertices_with_cubeoff(self, cube_off_mesh):

        zero_two = cube_off_mesh.get_halfedge(0, 2)
        assert zero_two.opposite().vertex().id == 0
        assert zero_two.opposite().prev().vertex().id == 2

        zero_one = cube_off_mesh.get_halfedge(0, 1)
        assert zero_one.opposite().vertex().id == 0
        assert zero_one.opposite().prev().vertex().id == 1

        four_one = cube_off_mesh.get_halfedge(4, 1)
        assert four_one.opposite().vertex().id == 4
        assert four_one.opposite().prev().vertex().id == 1
