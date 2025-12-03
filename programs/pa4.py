import sys
import os
from ICP_algo import solve_pa4

def main():
    # Expected command line arguments:
    # python pa4.py <bodyA_file> <bodyB_file> <mesh_file> <samples_file> <output_file>
    
    if len(sys.argv) != 6:
        print("Usage: python pa4.py <bodyA_file> <bodyB_file> <mesh_file> <samples_file> <output_file>")
        print("\nNote: Please provide 5 file paths as command line arguments.")
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
        # Call the solver function imported from icp_pa4.py
        solve_pa4(bodyA_file, bodyB_file, mesh_file, samples_file, output_file)
    except FileNotFoundError as e:
        print(f"ERROR: One or more required files not found: {e}")
        print("Please ensure your data files are correctly named and in the same directory.")
    except Exception as e:
        print(f"An unexpected error occurred during execution: {e}")


if __name__ == '__main__':
    # Add a check for the utility_functions module existence
    try:
        from utility_functions import read_mesh
    except ImportError:
        print("ERROR: utility_functions.py not found.")
        print("Please ensure your utility_functions.py is in the same directory.")
        sys.exit(1)
        
    main()