# Copyright (C) 2011 by Andrew Durdin
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


USAGE = """\
Usage: %s <input filename> <output filename>

<input filename> can be a .raw color table, a .tga file, or - for the identity
color table.

<output filename> can be a .raw color table or a .tga file.
"""


class ColorTable(object):
    def __init__(self, table=None):
        self.table = list(table) or []

    @classmethod
    def load_raw(cls, filename):
        from struct import unpack_from
        with file(filename, 'rb') as f:
            buf = f.read()

        assert len(buf) == 32 * 32 * 32 * 3, "Color correction file is not the expected size."
        pixel_fmt = "BBB"
        table = [unpack_from(pixel_fmt, buf, i * 3) for i in xrange(32 * 32 * 32)]
        return cls(table)

    @classmethod
    def load_tga(cls, filename):
        with file(filename, 'rb') as f:
            buf = f.read()

        from struct import unpack_from, calcsize
        offset = 0
        header_fmt = "<BBBHHBHHHHBB"
        header = unpack_from(header_fmt, buf, offset)
        (extra_len, color_map_present, image_type, color_map_start,
            color_map_len, color_map_bpp, x_origin, y_origin,
            width, height, bpp, descriptor) = header

        if (color_map_present or image_type != 2 or bpp != 24 or descriptor != 0):
            raise ValueError("Only 24-bit uncompressed TGA files are supported.")
        if (width != 32 * 32 or height != 32):
            raise ValueError("TGA files must be 1024 x 32 pixels.")

        offset = calcsize(header_fmt) + extra_len
        pixel_fmt = "BBB"
        pixels = [unpack_from(pixel_fmt, buf, offset + i * 3) for i in xrange(width * height)]
        pixels = [(r, g, b) for (b, g, r) in pixels]
        return cls(pixels)

    @classmethod
    def identity(cls):
        table = []
        mult = lambda v: int(255.0 / 31.0 * v + 0.5)
        for b in range(32):
            for g in range(32):
                table.extend([(mult(r), mult(g), mult(b)) for r in range(32)])
        return cls(table)

    def save_raw(self, filename):
        from struct import pack
        assert len(self.table) == 32 * 32 * 32, "Color correction table size is wrong."
        pixel_fmt = "BBB"
        data = [pack(pixel_fmt, *rgb) for rgb in self.table]

        with file(filename, 'wb') as f:
            f.write("".join(data))

    def save_tga(self, filename):
        from struct import pack, calcsize
        data = []
        header_fmt = "<BBBHHBHHHHBB"
        header = (0, 0, 2, 0, 0, 0, 0, 0, 32 * 32, 32, 24, 0)
        data.append(pack(header_fmt, *header))
        pixel_fmt = "BBB"
        pixels = [pack(pixel_fmt, rgb[2], rgb[1], rgb[0]) for rgb in self.table]
        data.extend(pixels)

        with file(filename, 'wb') as f:
            f.write("".join(data))


def main():
    import sys
    args = sys.argv[1:]
    if len(args) != 2:
        raise ValueError(USAGE % sys.argv[0])

    input_filename, output_filename = args
    if input_filename == '-':
        table = ColorTable.identity()
    elif input_filename.lower().endswith('.tga'):
        table = ColorTable.load_tga(input_filename)
    else:
        table = ColorTable.load_raw(input_filename)

    if output_filename.lower().endswith('.tga'):
        table.save_tga(output_filename)
    else:
        table.save_raw(output_filename)


if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        raise SystemExit(*e.args)
