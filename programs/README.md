# CISPA-4
Computer Integrated Surgery Programming Assignment 4

**Authors:** Maya Sharma and Anishka Bhartiya
**Date:** 12/4/25

## Installation Instructions
1. Make sure you have Python 3.8 or higher is installed on your system.
2. Install required dependencies:
   ```bash
   pip install numpy
   ```
3. Clone or download this repository to your local machine.
4. Place the input data files (`Problem4-BodyA.txt`, `Problem4-BodyB.txt`, `Problem4Mesh.sur`, `pa4-debug-X-SampleReadings.txt`) in the same directory as the source files.

## File Descriptions
**pa4.py** is the main script that runs the complete ICP algorithm with command-line arguments to process different datasets and generate output files with coordinates of s_k, c_k, and the magnitude of difference.

**unit_tests.py** has comprehensive tests validating `closest_point_on_triangle()` for vertex, edge, and interior projections, `closest_point_on_mesh()` with multiple triangles, edge cases, and single-triangle meshes, and more

**utility_functions.py** has helper functions from previous assignments including:
- File parsing for bodies, mesh, and sample readings
- Point-to-point registration (Arun's method)
- Frame transformations (`apply_transform`, `apply_inverse_transform`)
- Pivot calibration functions

**ICP_algo.py** is the core ICP implementation containing:
- `pre_calculate_dks()`: Precomputes probe tip positions in Body B coordinates
- `solve_pa4()`: Main ICP loop with iterative refinement
- Convergence checking and output generation

## Execution Instructions
To run the program and generate output in the specified PA#4 format:
```bash
python pa4.py -debug A
```
Replace `-debug A` with `-debug B`, `-unknown G`, etc., as needed for different datasets.

The output file `pa4-X-Output.txt` will be created containing:
- Header: `N_samps pa4-X-Output.txt`
- For each sample: `s_x s_y s_z    c_x c_y c_z    |s_k - c_k|`

## Dependencies
- **NumPy** (>=1.20.0): For numerical operations and linear algebra
- **Standard Python libraries**: sys, os, math

## References
```bibtex
@misc{benjamindkilleen2022Sep,
 author = {Killeen, Benjamin D.},
 title = {{cispa: Template for CIS I programming assignments at Johns Hopkins}},
 journal = {GitHub},
 year = {2022},
 month = {Sep},
 url = {https://github.com/benjamindkilleen/cispa}
}
```

## Notes
- The program implements the full iterative ICP algorithm as specified in PA#4
- Convergence tolerance defaults to 1e-5 with maximum 20 iterations
- Debug outputs include iteration progress and final mean residual error
- All mathematical derivations and algorithmic references follow the below sources

Killeen, B. D. (Sept. 8, 2022). Frame Transformations. Retrieved from https://benjamindkilleen.com/files/frame_transformations.pdf

K. S. Arun, T. S. Huang, and S. D. Blostein, “Least-squares fitting of two 3-D point sets,” IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. PAMI-9, no. 5, pp. 698–700, Sept. 1987.

Taylor, R. (1-73). Medical Robots Part 2 [Lecture presentation]. Computer Integrated Surgery 1, Johns Hopkins University

Taylor, R. (11). Calibration [Lecture presentation]. Computer Integrated Surgery 1, Johns Hopkins University

Taylor, R. (14). Calibration [Lecture presentation]. Computer Integrated Surgery 1, Johns Hopkins University