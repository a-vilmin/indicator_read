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


def make_cell(chunk, dims):
    hexa = vtkHexahedron()
    point_ids = make_ids(chunk, dims)

    for i in range(8):
        hexa.GetPointIds().SetId(i, point_ids[i])

    return hexa


def make_ids(chunk, dims):
    ids = []
    z_scalar = dims['DX'] * dims['DY']
    y_scalar = (dims['DX'] + 1) * dims['DY']

    ids.append((chunk['x'])+(chunk['y']*y_scalar)+(chunk['z']*z_scalar)+1)
    ids.append(ids[0] + 1)
    ids.append(ids[1] + dims['DX'] + 1)
    ids.append(ids[2] - 1)

    for i in range(4):
        ids.append(ids[i] + z_scalar)

    return ids


def add_points(x_lim, y_lim, z_lim, points):
    for z in range(z_lim+1):
        for y in range(y_lim+1):
            for x in range(x_lim+1):
                point = [x * DX, y * DY, z * DZ]
                points.InsertNextPoint(point)


def write_vtk(ugrid):
    writer = vtkUnstructuredGridWriter()
    writer.SetFileName("test_filter.vtk")
    writer.SetInputData(ugrid)
    writer.Write()


def main(bin_f, filter_vals, dims):
    read_file = open(bin_f, 'rb')

    ugrid = vtkUnstructuredGrid()
    points = vtkPoints()

    add_points(dims['DX'], dims['DY'], dims['DZ'], points)
    ugrid.SetPoints(points)

    values = vtkIntArray()
    values.SetName("Filtered Values")
    values.SetNumberOfComponents(1)

    count = 0

    while read_file.read(4):
        if count > 1000:
            break

        chunk = read_chunk(read_file)

        if chunk['i'] in filter_vals:
            values.InsertNextTuple1(chunk['i'])
            cell = make_cell(chunk, dims)
            ugrid.InsertNextCell(cell.GetCellType(), cell.GetPointIds())
            count += 1

        read_file.read(4)

    read_file.close()

    ugrid.GetCellData().AddArray(values)
    write_vtk(ugrid)


if __name__ == '__main__':
    from sys import argv
    filter_vals = range(8, 12)
    dims = {'DX': 500, 'DY': 500, 'DZ': 600}

    main(argv[1], filter_vals, dims)
