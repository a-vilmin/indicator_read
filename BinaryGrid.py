import numpy as np
from vtk import vtkImageData, vtkIntArray, vtkXMLImageDataWriter
from struct import unpack

DX = 2.0
DY = 2.0
DZ = 0.05


class BinaryGrid(object):

    def __init__(self, x_dim, y_dim, z_dim):
        self.dims = (x_dim, y_dim, z_dim)
        self.vals = np.empty((x_dim, y_dim, z_dim))

    def read_file(self, bin_f):
        bin_f = open(bin_f, 'rb')

        while bin_f.read(4):
            i = unpack('<I', bin_f.read(4))[0]
            x = unpack('<I', bin_f.read(4))[0]
            y = unpack('<I', bin_f.read(4))[0]
            z = unpack('<I', bin_f.read(4))[0]

            self.vals[x-1][y-1][z-1] = i
            bin_f.read(4)
        bin_f.close()

    def write_vtk(self):
        vtk = vtkImageData()

        vtk.SetSpacing(DX, DY, DZ)
        vtk.SetDimensions(self.dims[0]+1, self.dims[1]+1, self.dims[2]+1)

        array = vtkIntArray()
        array.SetName("Stratal Architecture")
        array.SetNumberOfComponents(1)

        for z in range(self.dims[2]-1, -1, -1):
            for y in range(0, self.dims[1]):
                for x in range(0, self.dims[0]):
                    val = self.vals[x][y][z]
                    array.InsertNextTuple1(val)
        vtk.GetCellData().AddArray(array)

        vtk_f = vtkXMLImageDataWriter()
        vtk_f.SetFileName("test_stratal.vti")
        vtk_f.SetInput(vtk)
        vtk_f.Write()

if __name__ == '__main__':
    from sys import argv

    tmp = BinaryGrid(500, 500, 600)
    tmp.read_file(argv[1])
    tmp.write_vtk()


