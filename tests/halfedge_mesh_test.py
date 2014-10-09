import halfedge_mesh
import pytest

class TestHalfedgeMesh:

    @pytest.fixture()
    def halfedge_cube_off_mesh(self, scope="module"):
        return halfedge_mesh.HalfedgeMesh("test_data/cube.off")

    def test_halfedge_mesh_cube_off_vertices_are_in_order(self,
                                                          halfedge_cube_off_mesh):

        vertices = halfedge_cube_off_mesh.vertices

        #cube vertices in order
        pts = [8, 12, 18, 1, -1, -1, 1, -1, 1, -1, -1, 1, -1, -1, -1, 1, 1,
               -0.999999, 0.999999, 1, 1.000001]

        for index in range(0, len(vertices), 3):
            # Vertex(a,b,c, index) index doesn't matter so it is set to zero
            assert vertices[index] == halfedge_mesh.Vertex(pts[index],
                                                           pts[index+1],
                                                           pts[index+2], 0)

    def test_halfedge_mesh_cube_off_vertices_in_facet_exists(self,
                                                             halfedge_cube_off_mesh):

        facets = halfedge_cube_off_mesh.facets
        vertices = halfedge_cube_off_mesh.vertices

        for index in range(len(facets)):
            # check that it's within the range of the number of vertices
            assert facets[index].a < len(vertices)
            assert (facets[index].a >= 0)

    def test_get_halfedge_returns_halfedge_with_correct_vertices(self):
        pass
