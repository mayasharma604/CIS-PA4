# imports
import numpy as np
from utility_functions import *
from ICP_algo import *
from ICP_iteration import *


# TRIANGEL TESTS

# test if the point is a vertex, the return is that same vertex
def testSameVertex():
    triangle = np.array([[0,0,0], [1,0,0], [0,1,0]])
    point = np.array([0,0,0])
    result = closest_point_on_triangle(point, triangle)
    assert np.allclose(result, [0,0,0])


# test if point is on the edge 
def test_same_edge_AB():
    # triangle vertices
    triangle = np.array([[0,0,0], [1,0,0], [0,1,0]])
    point = np.array([0.5, 0, 0])
    result = closest_point_on_triangle(point, triangle)
    # should return the same point on edge here
    assert np.allclose(result, [0.5, 0, 0])


# the return is the same point
def testPointInsideTriangle():
    
    triangle = np.array([[0,0,0], [1,0,0], [0,1,0]])
    point = np.array([0.3, 0.3, 0])
    result = closest_point_on_triangle(point, triangle)
    assert np.allclose(result, [0.3, 0.3, 0])


# test to seee if the point is outside of the triangle
# the return projects to the nearest edge or vertex
def test_closest_point_outside_triangle():
    tri = np.array([[0,0,0], [1,0,0], [0,1,0]])
    point = np.array([1,1,0])
    result = closest_point_on_triangle(point, tri)
    # should project to the midpoint of hypotenuse
    assert np.allclose(result, [0.5, 0.5, 0])

# this test is to see if thethe point is above the triangle
# the return projects the vertically onto plane
def testClosestPointAboveTriangle():
    triangle = np.array([[0,0,0], [1,0,0], [0,1,0]])
    
    query_point = np.array([0.3, 0.3, 2])
    
    # to get the closest point on triangle
    closestPoint = closest_point_on_triangle(query_point, triangle)
    assert np.allclose(closestPoint, [0.3, 0.3, 0])

# MESH TESTS BELOW

# test to make sure that the closest point on mesh function works for a simple test case scenario
def testClosestPointOnMeshSimple():
    # here is the vertex set up
    vertices = np.array([
        [0,0,0],
        [1,0,0],
        [0,1,0],
        [1,1,0]
    ])
    triangles = np.array([
        [0,1,2],
        [1,3,2]
    ])
    point = np.array([0.2, 0.2, 1.0])
    
    # getting the closest point on mesh
    closest, distance, idx = closest_point_on_mesh(point, vertices, triangles)

    # this point should project onto the first triangle
    assert np.allclose(closest, [0.2, 0.2, 0])

    assert idx == 0


# test that the closest point on mesh function works if the point is equally distant from two triangles
def test_closest_point_on_mesh_equal_dist():
    vertices = np.array([
        [0,0,0],
        [1,0,0],
        [0,1,0],
        [1,1,0]
    ])
    triangles = np.array([
        [0,1,2],
        [1,3,2]
    ])
    point = np.array([0.5, 0.5, 1.0])
    closest, distance, idx = closest_point_on_mesh(point, vertices, triangles)

#since the point is the same distance from boht triangles we can have either triangel as output
    assert np.allclose(closest, [0.5, 0.5, 0])
    assert np.isclose(distance, 1.0)
    assert idx in [0, 1]


#test the whole pipeline with synthetic data
def test_solve_pa4_direct_call():
    bodyA_file = "sample/Sample-BodyA.txt"
    bodyB_file = "sample/Sample-BodyB.txt"
    mesh_file  = "sample/SampleMeshFile.sur"
    sample_file = "sample/PA4-SampleReadings.txt"
    output_file = "sample/Sample_Output.txt"

    # call the function with sample files
    final_s, final_c = solve_pa4(
        bodyA_file,
        bodyB_file,
        mesh_file,
        sample_file,
        output_file,
        max_iterations=20,
        tolerance=1e-4
    )

    # check that both tip coordinates have 3 outputs and that the distances are finite
    assert os.path.exists(output_file), "Output file was not created"
    assert final_s.shape == final_c.shape
    assert final_s.shape[1] == 3
    dists = np.linalg.norm(final_s - final_c, axis=1)
    assert np.all(np.isfinite(dists))
    assert dists.mean() < 200
