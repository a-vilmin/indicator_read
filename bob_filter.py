from struct import unpack
from collections import defaultdict

from vtk import (vtkUnstructuredGrid, vtkHexahedron, vtkPoints,
                 vtkIntArray, vtkUnstructuredGridWriter)


DX = 2.0
DY = 2.0
DZ = 0.05


def read_chunk(bin_f):
    chunk = defaultdict(int)

    chunk['i'] = unpack('<I', bin_f.read(4))[0]
    chunk['x'] = unpack('<I', bin_f.read(4))[0]
    chunk['y'] = unpack('<I', bin_f.read(4))[0]
    chunk['z'] = unpack('<I', bin_f.read(4))[0]

    return chunk


def make_cell(chunk, index):
    hexa = vtkHexahedron()
    for i in range(8):
        hexa.GetPointIds().SetId(i, index)
        index += 1

    return hexa, index


def add_points(x, y, z, points):
    scaled_x = DX * x
    scaled_y = DY * y
    scaled_z = DZ * z

    points.InsertNextPoint([scaled_x, scaled_y, scaled_z])
    points.InsertNextPoint([scaled_x + DX, scaled_y, scaled_z])
    points.InsertNextPoint([scaled_x + DX, scaled_y + DY, scaled_z])
    points.InsertNextPoint([scaled_x, scaled_y + DY, scaled_z])

    points.InsertNextPoint([scaled_x, scaled_y, scaled_z + DZ])
    points.InsertNextPoint([scaled_x + DX, scaled_y, scaled_z + DZ])
    points.InsertNextPoint([scaled_x + DX, scaled_y + DY, scaled_z + DZ])
    points.InsertNextPoint([scaled_x, scaled_y + DY, scaled_z + DZ])


def write_vtk(ugrid):
    writer = vtkUnstructuredGridWriter()
    writer.SetFileName("test_filter.vtk")
    writer.SetInput(ugrid)
    writer.Write()


def main(bin_f, filter_vals):
    read_file = open(bin_f, 'rb')

    ugrid = vtkUnstructuredGrid()
    points = vtkPoints()
    values = vtkIntArray()

    values.SetName("Filtered Values")
    values.SetNumberOfComponents(1)
    index = 0

    while read_file.read(4):
        chunk = read_chunk(read_file)

        if chunk['i'] in filter_vals:
            values.InsertNextTuple1(chunk['i'])
            add_points(chunk['x'], chunk['y'], chunk['z'], points)

            cell, index = make_cell(chunk, index)
            ugrid.InsertNextCell(cell.GetCellType(), cell.GetPointIds())

        read_file.read(4)

    read_file.close()

    ugrid.SetPoints(points)
    ugrid.GetCellData().AddArray(values)
    write_vtk(ugrid)


if __name__ == '__main__':
    from sys import argv
    filter_vals = range(8, 12)

    main(argv[1], filter_vals)
