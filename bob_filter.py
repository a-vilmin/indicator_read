from struct import unpack
from collections import defaultdict
from vtk import vtkUnstructuredGrid, vtkHexahedron, vtkPoints, vtkIntArray


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

    return hexa


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


def main(bin_f, filter_vals):
    read_file = open(bin_f, 'rb')
    read_file.read(4)

    ugrid = vtkUnstructuredGrid()
    points = vtkPoints()
    values = vtkIntArray()
    index = 0

    while bin_f.read(4):
        chunk = read_chunk(bin_f)

        if chunk['i'] in filter_vals:
            values.InsertNextTuple1(chunk['i'])
            add_points(chunk['x'], chunk['y'], chunk['z'], points)

            cell = make_cell(chunk, index)
            ugrid.InsertNextCell(cell.GetCellType(), cell.GetPointIds())
        else:
            continue

        bin_f.read(4)
