import numpy as np
from vtk import vtkImageData, vtkIntArray, vtkXMLImageDataWriter
from struct import unpack


class BinaryGrid(object):
    """Class for parsing a *.out binary file created for stratal architecture
    models from Wright State
    :self.dims: dimensions of grid
    :self.vals: numpy array to hold indicator values
    """
    def __init__(self, x_dim=500, y_dim=500, z_dim=600):
        """initializes dimensions and empty value array sized to dimensions.
        Default dimensions are 500X500X600"""

        self.dims = (x_dim, y_dim, z_dim)
        self.vals = np.empty((x_dim, y_dim, z_dim))

    def read_file(self, bin_f):
        """Takes filename and parses into self.vals array. Operates under bin file
        being structured with "\n . . . int int int \n . . ." bits are read
        little endian"""

        bin_f = open(bin_f, 'rb')

        # newlines are read as 4 for byte padding
        while bin_f.read(4):
            i = unpack('<I', bin_f.read(4))[0]
            x = unpack('<I', bin_f.read(4))[0]
            y = unpack('<I', bin_f.read(4))[0]
            z = unpack('<I', bin_f.read(4))[0]

            self.vals[x-1][y-1][z-1] = i
            bin_f.read(4)
        bin_f.close()

    def write_vtk(self, DX=2.0, DY=2.0, DZ=0.05):
        """Reads cell data from vals array and writes into a VTK file called
        'Stratal_Arch.vti' and is a structure grid object. Spacing defaults
        are 2.0/2.0/0.05"""

        vtk_obj = vtkImageData()

        vtk_obj.SetSpacing(DX, DY, DZ)
        vtk_obj.SetDimensions(self.dims[0]+1, self.dims[1]+1, self.dims[2]+1)

        # Start writing from the top of the object to match output from Eclipse
        vtk_obj.SetOrigin(0, 0, self.dims[2]+1)

        array = vtkIntArray()
        array.SetName("Stratal Architecture")
        array.SetNumberOfComponents(1)

        for z in range(0, self.dims[2]):
            for y in range(0, self.dims[1]):
                for x in range(0, self.dims[0]):
                    val = self.vals[x][y][z]
                    array.InsertNextTuple1(val)
        vtk_obj.GetCellData().AddArray(array)

        vtk_f = vtkXMLImageDataWriter()
        vtk_f.SetFileName("Stratal_Arch.vti")
        vtk_f.SetInputData(vtk_obj)
        vtk_f.Write()

if __name__ == '__main__':
    from sys import argv

    tmp = BinaryGrid()
    tmp.read_file(argv[1])
    tmp.write_vtk()
