
# Stratal Architecture Scripting

* BinaryGrid.py for Stratal Indicator binary file parsing
* Stratal_Perm.py for Permeability ASCII type parsing 


## Running BinaryGrid.py
1. Requires Numpy, VTK Python 6.x or higher, and Python 2.7 (will not run on Python 3!)

2. Runs on binary .out type as created by Wright State research with format:  
   < \n+ 3 padding bytes -> int -> int -> int -> \n + 3 padding bytes>               
    and where bytes are packed little endian.
    
3. Running default values for dimensions of 500X500X600 cells and spacing of 2/2/0.05 can be run with "python BinaryGrid.py < file location >"
4. To change defaults, either import BinaryGrid from BinaryGrid.py and create custom BinaryGrid objects or consult source code and edit as needed.


## Running Stratal_Perm.py
1. Requires Numpy, VTK Python 6.x or higher, and Python 2.7 (will not run on Python 3!)
2. Runs on the ASCII type formatted "value X Y Z"
3. Same default values as BinaryGrid.py
4. Edit the function "main" or import "create_array" and "write_vtk" to utilize them with custom values.

