import os
import sys
import argparse
from ICP_algo import *

'''
Created on November 6, 2025
Author: Maya Sharma
Parameters: none
Returns: none
Summary: main function to handle command line arguments and run ICP matching
'''
def main():
   
    parses = argparse.ArgumentParser(description='Prog Assignment 3')
    parses.add_argument('--debug', type=str, choices=['A', 'B', 'C', 'D', 'E', 'F'], 
                       help='debug case that need to be run (A-F)')
    parses.add_argument('--unknown', type=str, choices=['G', 'H', 'J'], 
                       help='the unknown case that need to be run (G, H, J)')
    
    args = parses.parse_args()
    
    if not args.debug and not args.unknown:
        print("ERROR! Please specify if you want to run the debug files (--debug) or the unknown files (--unknown).")
        parses.print_help()
        sys.exit(1)
    
    if args.debug:
        case = args.debug
        file_type = "Debug"
    else:
        case = args.unknown
        file_type = "Unknown"
    
    data_dir = '2025_PA345_Student_Data'
    #body A
    bodyA_file = os.path.join(data_dir, 'Problem3-BodyA.txt')
    # body B
    bodyB_file = os.path.join(data_dir, 'Problem3-BodyB.txt')
    # for the mesh file
    mesh_file = os.path.join(data_dir, 'Problem3Mesh.sur')
    # sample readnig file
    samples_file = os.path.join(data_dir, f'PA3-{case}-{file_type}-SampleReadingsTest.txt')
    output_file = f'OUTPUT/PA3-{case}-{file_type}-Output.txt'
    
    required_files = [bodyA_file, bodyB_file, mesh_file, samples_file]
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    # check if there are any missnig files
    if missing_files:
        print(f"ERROR! You are  Missing {len(missing_files)} number of input file(s):")
        for missing in missing_files:
            print(f"  - {missing}")
        sys.exit(1)
    
    os.makedirs('OUTPUT', exist_ok=True)
    
    # use try catch in case of error
    try:
        results = solve_pa3(
            bodyA_file=bodyA_file,
            bodyB_file=bodyB_file, 
            mesh_file=mesh_file,
            sample_readings_file=samples_file,
            output_file=output_file
        )
        
        # print
        distances = [result['distance'] for result in results]
        average_dist = sum(distances) / len(distances)
        maximum_dist = max(distances)
        minimum_dist = min(distances)
        
        # in case of error
    except Exception as e:
        print(f"ERROR! during processing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
    #debug and unkown run through command line