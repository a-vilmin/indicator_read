from sys import argv


def test_read(f):
    with open(f, "rb") as binary:
        binary.seek(0)

        while binary.read(4):
            i = int.from_bytes(binary.read(4), byteorder='little')
            x = int.from_bytes(binary.read(4), byteorder='little')
            y = int.from_bytes(binary.read(4), byteorder='little')
            z = int.from_bytes(binary.read(4), byteorder='little')
            binary.read(4)

            string = 'x={0}  y={1}  z={2}  i={3}'.format(x, y, z, i)
            print(string)

if __name__ == '__main__':
    test_read(argv[1])
