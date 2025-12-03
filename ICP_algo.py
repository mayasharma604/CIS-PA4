



# import numpy as np

# from utility_functions import *

# '''
# Created on November 6, 2025
# Author: Anishka Bhartiya
# Parameters: point and triangle_vertices (diensions 3,3)
# Returns: the closest point on triangle to given point
# Summary: computes closest point that is on thetriangle to given point
# '''
# def closest_point_on_triangle(point, triangle_vertices):
    
#     #triangle verts
#     A, B, C = triangle_vertices
    
#     AB = B - A
    
#     AC = C - A
#     AP = point - A
    
#     d_1 = np.dot(AB, AP)
#     d_2 = np.dot(AC, AP)
    
#     if d_1 <= 0.0 and d_2 <= 0.0:
#         return A
    
#     BP = point - B
    
#     d3 = np.dot(AB, BP)
#     d4 = np.dot(AC, BP)
#     if d3 >= 0.0 and d4 <= d3:
#         return B
    
    
#     CP = point - C
    
#     d5 = np.dot(AB, CP)
#     d6 = np.dot(AC, CP)
#     if d6 >= 0.0 and d5 <= d6:
#         return C
    
#     vc = d_1 * d4 - d3 * d_2
    
#     if vc <= 0.0 and d_1 >= 0.0 and d3 <= 0.0:
#         # fraction along AB is
#         v = d_1 / (d_1 - d3)
#         return A + v * AB
    
#     vb = d5 * d_2 - d_1 * d6
    
#     if vb <= 0.0 and d_2 >= 0.0 and d6 <= 0.0:
        
#         w = d_2 / (d_2 - d6)
#         return A + w * AC
    
#     va = d3 * d6 - d5 * d4
#     if va <= 0.0 and (d4 - d3) >= 0.0 and (d5 - d6) >= 0.0:
       
#         w = (d4 - d3) / ((d4 - d3) + (d5 - d6))
#         return B + w * (C - B)
    
#     denom = 1.0 / (va + vb + vc)
    
#     v = vb * denom
#     w = vc * denom
    
#     return A + v * AB + w * AC

# '''
# Created November 6, 2025
# Author: Anishka Bhartiya
# Parameters: takes in the  point, vertcies on mesh   and  triangles on mesh  
# Returns: returns the closest point that's on mesh, what the distnce to that point is, and that triangles' index
# Summary: this functions finds what the  closest point on the mesh to  agiven point
# '''
# def closest_point_on_mesh(point, vertices, triangles):
    
#     min_distance = float('inf')
#     close_pt = None
#     closest_triangle_idx = -1
    
#     for i, triangle in enumerate(triangles):
        
#         triangle_vertices = vertices[triangle]
        
        
#         candidate_point = closest_point_on_triangle(point, triangle_vertices)
# #
#         distance = np.linalg.norm(point - candidate_point)
        
#         if distance < min_distance:
#             min_distance = distance
#             close_pt = candidate_point
#             closest_triangle_idx = i
    
#     return close_pt, min_distance, closest_triangle_idx

# '''
# Created on November 7, 2025
# Author: Maya Sharma
# Parameters: takes in bodyA_file, bodyB_file, the mesh file, sample readings file, and the output file
# Returns: results the list that has d_k, s_k and ck
# Summary: main function for the ICP matching algorithm
# '''
# def solve_pa3(bodyA_file, bodyB_file, mesh_file, sample_readings_file, output_file):
    
#     vertices, triangles, neighbours = read_mesh(mesh_file)
    
#     # body files reading in
#     A_markers, A_tip = read_body(bodyA_file)
    
#     B_markers, B_tip = read_body(bodyB_file)
    
#     frames, Ns, Nsamps = read_sample_readings(sample_readings_file)
    
#     # markers #
#     N_A = len(A_markers)
#     N_B = len(B_markers)
    
#     F_reg_R = np.eye(3)  
#     F_reg_t = np.zeros(3)  
    
#     results = []
    
#     # this loop processes the data per each frmae
#     for k in range(Nsamps):
#         frame_data = frames[k]
        
#         a_markers_tracker = frame_data[:N_A]  
#         b_markers_tracker = frame_data[N_A:N_A+N_B]  
        
#         # gets RA and tA
#         R_A, t_A = register_points(A_markers, a_markers_tracker)
#         # calculates RB and tB
#         R_B, t_B = register_points(B_markers, b_markers_tracker)
        
#         R_B_inv, t_B_inv = apply_inverse_transform(R_B, t_B)
        
#         A_tip_transformed = apply_transform(R_A, t_A, A_tip.reshape(1, -1))[0]
#         d_k = apply_transform(R_B_inv, t_B_inv, A_tip_transformed.reshape(1, -1))[0]
        
#        # applies the overall transform that is registration for calculation of sk here
#         s_k = apply_transform(F_reg_R, F_reg_t, d_k.reshape(1, -1))[0]
        
#         # find what the closest point on the mesh is
#         c_k, distance, triangle_idx = closest_point_on_mesh(s_k, vertices, triangles)
        
#         # add results
#         results.append({
#             'd_k': d_k,
#             's_k': s_k, 
#             'c_k': c_k,
#             'distance': distance
#         })
    
#     with open(output_file, 'w') as f:
#         f.write(f"{Nsamps} {output_file}\n")
        
#         for result in results:
#             # get the values from dictionary that had the results
#             d = result['d_k']
#             c = result['c_k']
#             dist = result['distance']
            
#             # saves values and write them in the same format as the answer txt files
#             # rou ding to two deci points to match the output answer files formatting
#             f.write(f"{d[0]:8.2f} {d[1]:8.2f} {d[2]:8.2f}    ")
#             f.write(f"{c[0]:8.2f} {c[1]:8.2f} {c[2]:8.2f}    ")
            
#             # rounding to three deci points to match Prof Taylor's answer output files formatting
#             f.write(f"{dist:8.3f}\n")
    
#     return results

import numpy as np
from utility_functions import (
    read_mesh,
    read_body,
    read_sample_readings,
    register_points,
    apply_transform,
    apply_inverse_transform
)

# --- ICP Matching Functions (from your PA#3) ---

'''
Created on November 6, 2025
Author: Anishka Bhartiya
Parameters: point and triangle_vertices (dimensions 3,3)
Returns: the closest point on triangle to given point
Summary: computes closest point that is on the triangle to given point
'''
def closest_point_on_triangle(point, triangle_vertices):
    # triangle verts
    A, B, C = triangle_vertices
    
    AB = B - A
    AC = C - A
    AP = point - A
    
    d_1 = np.dot(AB, AP)
    d_2 = np.dot(AC, AP)
    
    if d_1 <= 0.0 and d_2 <= 0.0:
        return A
    
    BP = point - B
    
    d3 = np.dot(AB, BP)
    d4 = np.dot(AC, BP)
    if d3 >= 0.0 and d4 <= d3:
        return B
    
    
    CP = point - C
    
    d5 = np.dot(AB, CP)
    d6 = np.dot(AC, CP)
    if d6 >= 0.0 and d5 <= d6:
        return C
    
    vc = d_1 * d4 - d3 * d_2
    
    if vc <= 0.0 and d_1 >= 0.0 and d3 <= 0.0:
        # fraction along AB is
        v = d_1 / (d_1 - d3)
        return A + v * AB
    
    vb = d5 * d_2 - d_1 * d6
    
    if vb <= 0.0 and d_2 >= 0.0 and d6 <= 0.0:
        
        w = d_2 / (d_2 - d6)
        return A + w * AC
    
    va = d3 * d6 - d5 * d4
    if va <= 0.0 and (d4 - d3) >= 0.0 and (d5 - d6) >= 0.0:
        
        w = (d4 - d3) / ((d4 - d3) + (d5 - d6))
        return B + w * (C - B)
    
    denom = 1.0 / (va + vb + vc)
    
    v = vb * denom
    w = vc * denom
    
    return A + v * AB + w * AC

'''
Created November 6, 2025
Author: Anishka Bhartiya
Parameters: takes in the point, vertcies on mesh and triangles on mesh 
Returns: returns the closest point that's on mesh, what the distnce to that point is, and that triangles' index
Summary: this functions finds what the closest point on the mesh to a given point
'''
def closest_point_on_mesh(point, vertices, triangles):
    
    min_distance = float('inf')
    close_pt = None
    closest_triangle_idx = -1
    
    for i, triangle in enumerate(triangles):
        
        # indices in the triangle array are 0-based for numpy indexing
        triangle_vertices = vertices[triangle]
        
        candidate_point = closest_point_on_triangle(point, triangle_vertices)
        distance = np.linalg.norm(point - candidate_point)
        
        if distance < min_distance:
            min_distance = distance
            close_pt = candidate_point
            closest_triangle_idx = i
    
    return close_pt, min_distance, closest_triangle_idx

# --- PA#4 Specific Functions ---

'''
Created on December 2, 2025
Author: AI Assistant
Parameters: Body A/B markers and tip, sample readings data
Returns: Array of d_k points (N_samps x 3)
Summary: Pre-calculates the pointer tip position d_k in the Body B coordinate system for all sample frames.
This value is constant throughout the ICP iterations.
'''
def pre_calculate_dks(A_markers, A_tip, B_markers, B_tip, frames, Nsamps, N_A, N_B):
    d_k_points = []
    
    # Pre-calculate R_A, t_A, R_B, t_B and d_k for all samples
    for k in range(Nsamps):
        frame_data = frames[k]
        
        a_markers_tracker = frame_data[:N_A]
        b_markers_tracker = frame_data[N_A:N_A+N_B]
        
        # 1. Calculate F_A,k and F_B,k (poses of rigid bodies in tracker frame)
        R_A, t_A = register_points(A_markers, a_markers_tracker)
        R_B, t_B = register_points(B_markers, b_markers_tracker)
        
        # 2. Calculate F_B,k_inv
        R_B_inv, t_B_inv = apply_inverse_transform(R_B, t_B)
        
        # 3. Calculate d_k = F_B,k_inv * F_A,k * A_tip
        # Transform A_tip from Body A to Tracker frame
        A_tip_transformed = apply_transform(R_A, t_A, A_tip.reshape(1, -1))[0]
        # Transform result from Tracker frame to Body B frame (d_k)
        d_k = apply_transform(R_B_inv, t_B_inv, A_tip_transformed.reshape(1, -1))[0]
        
        d_k_points.append(d_k)
        
    return np.array(d_k_points)

'''
Created on December 2, 2025
Author: AI Assistant
Parameters: takes in bodyA_file, bodyB_file, the mesh file, sample readings file, and the output file,
            plus max_iterations and a tolerance for convergence.
Returns: The final s_k and c_k points
Summary: main function for the complete ICP algorithm (PA#4)
'''
def solve_pa4(bodyA_file, bodyB_file, mesh_file, sample_readings_file, output_file, max_iterations=20, tolerance=1e-5):
    
    # 1. Initialization and Data Loading
    vertices, triangles, _ = read_mesh(mesh_file)
    A_markers, A_tip = read_body(bodyA_file)
    B_markers, B_tip = read_body(bodyB_file)
    frames, _, Nsamps = read_sample_readings(sample_readings_file)
    
    N_A = len(A_markers)
    N_B = len(B_markers)

    # 2. Pre-calculate d_k points (constant for all iterations)
    d_k_points = pre_calculate_dks(A_markers, A_tip, B_markers, B_tip, frames, Nsamps, N_A, N_B)
    
    # 3. ICP Setup: F_reg is initialized to identity
    R_reg = np.eye(3) 
    t_reg = np.zeros(3)
    prev_mean_distance = float('inf')

    print("Starting ICP iterations...")
    
    # 4. ICP Iteration Loop
    for iteration in range(max_iterations):
        
        # 4.a. Matching step: Find s_k and corresponding closest points c_k
        s_k_points = []
        c_k_points = []
        distances = []
        
        for d_k in d_k_points:
            # s_k = F_reg * d_k
            s_k = apply_transform(R_reg, t_reg, d_k.reshape(1, -1))[0]
            
            # c_k = closest point on mesh to s_k
            c_k, distance, _ = closest_point_on_mesh(s_k, vertices, triangles)
            
            s_k_points.append(s_k)
            c_k_points.append(c_k)
            distances.append(distance)
        
        c_k_points_array = np.array(c_k_points)
        
        # 4.b. Registration step: Compute new F_reg that maps d_k -> c_k
        # d_k_points is the source (moving) and c_k_points_array is the target (fixed)
        R_reg_new, t_reg_new = register_points(d_k_points, c_k_points_array)
        
        # 4.c. Check for convergence
        mean_distance = np.mean(distances)
        
        # Convergence criterion: change in the mean distance is below tolerance
        if abs(prev_mean_distance - mean_distance) < tolerance:
            print(f"ICP converged after {iteration + 1} iterations. Mean distance: {mean_distance:.4f}")
            break
            
        # Update F_reg and previous distance
        R_reg = R_reg_new
        t_reg = t_reg_new
        prev_mean_distance = mean_distance
        
        print(f"Iteration {iteration + 1}: Mean distance = {mean_distance:.4f}")

    else:
        print(f"ICP finished after maximum {max_iterations} iterations without meeting tolerance. Final mean distance: {prev_mean_distance:.4f}")

    # 5. Final Output Generation (s_k, c_k, |s_k - c_k|)
    final_s_k_points = []
    final_c_k_points = []
    
    # Re-run matching with the final F_reg to ensure final s_k and c_k are used for output.
    for d_k in d_k_points:
        s_k = apply_transform(R_reg, t_reg, d_k.reshape(1, -1))[0]
        c_k, _, _ = closest_point_on_mesh(s_k, vertices, triangles)
        final_s_k_points.append(s_k)
        final_c_k_points.append(c_k)
        
    final_s_k_points = np.array(final_s_k_points)
    final_c_k_points = np.array(final_c_k_points)
    
    # Write output to file in PA#4 format
    with open(output_file, 'w') as f:
        f.write(f"{Nsamps} {output_file}\n")
        
        for s, c in zip(final_s_k_points, final_c_k_points):
            # Format: sx sy sz cx cy cz |s_k - c_k|
            diff_mag = np.linalg.norm(s - c)
            
            f.write(f"{s[0]:8.2f} {s[1]:8.2f} {s[2]:8.2f}    ")
            f.write(f"{c[0]:8.2f} {c[1]:8.2f} {c[2]:8.2f}    ")
            f.write(f"{diff_mag:8.3f}\n")
            
    return final_s_k_points, final_c_k_points