import numpy as np
from vtk import vtkImageData, vtkFloatArray, vtkXMLImageDataWriter
from sys import argv


def create_array(read_f, x_dim=500, y_dim=500, z_dim=600):
    arr = np.empty((z_dim, y_dim, x_dim))

    for line in read_f.readlines():
        i, x, y, z = line.split()

        arr[int(z)-1][int(y)-1][int(x)-1] = float(i)
    return arr


def write_vtk(arr, DX=2.0, DY=2.0, DZ=.05, x_dim=500, y_dim=500, z_dim=600):
    vtk = vtkImageData()

    vtk.SetSpacing(DX, DY, DZ)
    vtk.SetDimensions(x_dim+1, y_dim+1, z_dim+1)
    vtk.SetOrigin(0, 0, 0)

    vtk_arr = vtkFloatArray()
    vtk_arr.SetName("Stratal Permiablities")
    vtk_arr.SetNumberOfComponents(1)

    for z in range(z_dim):
        for y in range(y_dim):
            for x in range(x_dim):
                vtk_arr.InsertNextTuple1(arr[z][y][x])
    vtk.GetCellData().AddArray(vtk_arr)

    vtk_writer = vtkXMLImageDataWriter()
    vtk_writer.SetFileName("Stratal_Perms.vti")
    vtk_writer.SetInputData(vtk)
    vtk_writer.Write()


def main():
    read_f = open(argv[1], 'r')

    np_arr = create_array(read_f)

    write_vtk(np_arr)

if __name__ == '__main__':
    main()
