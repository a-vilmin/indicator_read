import numpy as np
from vtk import vtkImageData, vtkIntArray, vtkXMLImageDataWriter
from struct import unpack
from collections import defaultdict

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
        vtk_objs = defaultdict(vtkImageData)

        for i in range(0, 6):
            vtk_objs['vtk'+str(i)] = vtkImageData()

        z_hold = 0
        for key, vtk in vtk_objs.iteritems():
            vtk.SetSpacing(DX, DY, DZ)
            vtk.SetDimensions(self.dims[0]+1, self.dims[1]+1, 101)

            vtk.SetOrigin(0, 0, z_hold*DZ)
            array = vtkIntArray()
            array.SetName("Stratal Architecture")
            array.SetNumberOfComponents(1)

            for z in range(z_hold, z_hold+100):
                for y in range(0, self.dims[1]):
                    for x in range(0, self.dims[0]):
                        val = self.vals[x][y][z]
                        array.InsertNextTuple1(val)
            vtk.GetCellData().AddArray(array)
            z_hold += 100

        for key, vtk in vtk_objs.iteritems():
            vtk_f = vtkXMLImageDataWriter()
            vtk_f.SetFileName(key+".vti")
            vtk_f.SetInput(vtk)
            vtk_f.Write()

if __name__ == '__main__':
    from sys import argv

    tmp = BinaryGrid(500, 500, 600)
    tmp.read_file(argv[1])
    tmp.write_vtk()


