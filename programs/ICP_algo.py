import numpy as np
from programs.utility_functions import *

'''
Created on November 6, 2025
Author: Anishka Bhartiya
Parameters: point and triangle_vertices (diensions 3,3)
Returns: the closest point on triangle to given point
Summary: computes closest point that is on thetriangle to given point
'''
def closest_point_on_triangle(point, triangle_vertices):
    
    #triangle verts
    A, B, C = triangle_vertices
    
    AB = B - A
    
    AC = C - A
    AP = point - A
    
    d_1 = np.dot(AB, AP)
    d_2 = np.dot(AC, AP)
    
    # check if the point is closest to the first vertex (A)
    if d_1 <= 0.0 and d_2 <= 0.0:
        return A
    
    BP = point - B
    
    # check if the point is closest to the second vertex (B)
    d3 = np.dot(AB, BP)
    d4 = np.dot(AC, BP)
    if d3 >= 0.0 and d4 <= d3:
        return B
    
    
    CP = point - C
    
    # check if the point is closest to the third vertex (C)
    d5 = np.dot(AB, CP)
    d6 = np.dot(AC, CP)
    if d6 >= 0.0 and d5 <= d6:
        return C
    
    vc = d_1 * d4 - d3 * d_2
    
     # check if the point is closest to the AB edge
    if vc <= 0.0 and d_1 >= 0.0 and d3 <= 0.0:
        v = d_1 / (d_1 - d3)
        return A + v * AB
    
    vb = d5 * d_2 - d_1 * d6
    
    # check if the point is closest to the AC edge
    if vb <= 0.0 and d_2 >= 0.0 and d6 <= 0.0:
        
        w = d_2 / (d_2 - d6)
        return A + w * AC
    
    va = d3 * d6 - d5 * d4

    # check if the point is closest to the BC edge
    if va <= 0.0 and (d4 - d3) >= 0.0 and (d5 - d6) >= 0.0:
       
        w = (d4 - d3) / ((d4 - d3) + (d5 - d6))
        return B + w * (C - B)
    
    # otherwise, point is projected in the area of the triangle
    denom = 1.0 / (va + vb + vc)
    
    v = vb * denom
    w = vc * denom
    
    return A + v * AB + w * AC

'''
Created November 6, 2025
Author: Anishka Bhartiya
Parameters: takes in the  point, vertcies on mesh   and  triangles on mesh  
Returns: returns the closest point that's on mesh, what the distnce to that point is, and that triangles' index
Summary: this functions finds what the  closest point on the mesh to  agiven point
'''
def closest_point_on_mesh(point, vertices, triangles):
    
    min_distance = float('inf')
    close_pt = None
    closest_triangle_idx = -1
    
    # compare the minimum distance from the point to each triangle in the mesh
    for i, triangle in enumerate(triangles):
        
        triangle_vertices = vertices[triangle]
        
        
        candidate_point = closest_point_on_triangle(point, triangle_vertices)
#
        distance = np.linalg.norm(point - candidate_point)
        
        # update indices if current triangle has a smaller distance
        if distance < min_distance:
            min_distance = distance
            close_pt = candidate_point
            closest_triangle_idx = i
    
    return close_pt, min_distance, closest_triangle_idx

'''
Created on November 7, 2025
Author: Maya Sharma
Parameters: takes in bodyA_file, bodyB_file, the mesh file, sample readings file, and the output file
Returns: results the list that has d_k, s_k and ck
Summary: main function for the ICP matching algorithm
'''
def solve_pa3(bodyA_file, bodyB_file, mesh_file, sample_readings_file, output_file):
    
    vertices, triangles, neighbours = read_mesh(mesh_file)
    
    # body files reading in
    A_markers, A_tip = read_body(bodyA_file)
    
    B_markers, B_tip = read_body(bodyB_file)
    
    frames, Ns, Nsamps = read_sample_readings(sample_readings_file)
    
    # markers #
    N_A = len(A_markers)
    N_B = len(B_markers)
    
    F_reg_R = np.eye(3)  
    F_reg_t = np.zeros(3)  
    
    results = []
    
    # this loop processes the data per each frmae
    for k in range(Nsamps):
        frame_data = frames[k]
        
        a_markers_tracker = frame_data[:N_A]  
        b_markers_tracker = frame_data[N_A:N_A+N_B]  
        
        # gets RA and tA
        R_A, t_A = register_points(A_markers, a_markers_tracker)
        # calculates RB and tB
        R_B, t_B = register_points(B_markers, b_markers_tracker)
        
        R_B_inv, t_B_inv = apply_inverse_transform(R_B, t_B)
        
        A_tip_transformed = apply_transform(R_A, t_A, A_tip.reshape(1, -1))[0]
        d_k = apply_transform(R_B_inv, t_B_inv, A_tip_transformed.reshape(1, -1))[0]
        
       # applies the overall transform that is registration for calculation of sk here
        s_k = apply_transform(F_reg_R, F_reg_t, d_k.reshape(1, -1))[0]
        
        # find what the closest point on the mesh is
        c_k, distance, triangle_idx = closest_point_on_mesh(s_k, vertices, triangles)
        
        # add results
        results.append({
            'd_k': d_k,
            's_k': s_k, 
            'c_k': c_k,
            'distance': distance
        })
    
    with open(output_file, 'w') as f:
        f.write(f"{Nsamps} {output_file}\n")
        
        for result in results:
            # get the values from dictionary that had the results
            d = result['d_k']
            c = result['c_k']
            dist = result['distance']
            
            # saves values and write them in the same format as the answer txt files
            # rou ding to two deci points to match the output answer files formatting
            f.write(f"{d[0]:8.2f} {d[1]:8.2f} {d[2]:8.2f}    ")
            f.write(f"{c[0]:8.2f} {c[1]:8.2f} {c[2]:8.2f}    ")
            
            # rounding to three deci points to match Prof Taylor's answer output files formatting
            f.write(f"{dist:8.3f}\n")
    
    return results
