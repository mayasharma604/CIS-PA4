import sys
import os
from ICP_iteration import solve_pa4

def main():
   

    if len(sys.argv) != 6:
        print("please use the terminal command python pa4.py bodyA_file bodyB_file mesh_file samples_file output_file")
        print("please give 5 file paths as command line args")
        sys.exit(1)
    
    bodyA_file = sys.argv[1]
    bodyB_file = sys.argv[2]
    mesh_file = sys.argv[3]
    samples_file = sys.argv[4]
    output_file = sys.argv[5]

    print(f"Running PA#4 ICP with files:")
    print(f"  Body A: {bodyA_file}")
    print(f"  Body B: {bodyB_file}")
    print(f"  Mesh: {mesh_file}")
    print(f"  Samples: {samples_file}")
    print(f"  Output: {output_file}")
    print("-" * 30)

    try:

        solve_pa4(bodyA_file, bodyB_file, mesh_file, samples_file, output_file)
    except FileNotFoundError as e:
        print(f"one or more of the required files for this program to run wasn't found: {e}")
        print(" make sure your your data files are correctly named and in the same directory as this main!.")
    except Exception as e:
        print(f"an unexpected error occurred during execution: {e}")


if __name__ == '__main__':

    try:
        from utility_functions import read_mesh
    except ImportError:
        print("utility_functions file wasn't found.")
        print(" make sure you utility functions python file is in the same directory!.")
        sys.exit(1)
        
    main()