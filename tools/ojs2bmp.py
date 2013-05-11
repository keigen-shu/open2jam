#!/usr/bin/env python3

import os, sys, struct
import BMPtoolkit

"""
O2Jam OJS/OJT to BMP Converter
Script by Keigen Shu

Main Header [8 bytes]
0x0 ~ 0x1 >> 01 00 (File type; some files have 00 00) *[1]
0x2 ~ 0x3 >> 55 05 (Possibly bitmap bit size, ?1 R5 G5 B5)

0x4 ~ 0x5 >> Image count
0x6 ~ 0x7 >> Transparent mask color
0x7 ~ 0x? >> Image headers
0x? ~ EOF >> Image data

Image Header [20 bytes for each image]
0x00 ~ 0x01 - origin X position (signed integer) *[2]
0x02 ~ 0x03 - origin Y position (signed integer) *[2]
0x04 ~ 0x05 - Image width   (signed integer) *[2]
0x06 ~ 0x07 - Image height  (signed integer) *[2]
0x08 ~ 0x0B - Image address (starts with zero after all header data, unless file type is 00 00) *[1]
0x0C ~ 0x0F - Image size    (in bytes)
0x10 ~ 0x13 - 00 00 00 00   (unused)

*[1] For file type 00 00:
If the address for the first image data is not zero, then that address MAY be
relative to the beginning of the file (+= 8 + Image count * 20).

*[2] Something that I remember:
One of these things, when set to negative causes the resulting image to be drawn
in a different manner; the origin point or the bitmap order might change.

"""


if len(sys.argv) < 2:
    sys.exit('Usage: %s FILES' % sys.argv[0])

for f in range(len(sys.argv)-1):

    if not os.path.exists(sys.argv[1+f]):
        sys.exit('ERROR: File %s was not found!' % sys.argv[1+f])
    else:
        print("File:",sys.argv[1+f])

    srcfile = open(sys.argv[1+f],"rb")

    fileHead = struct.unpack("4H", srcfile.read(8))

    type = fileHead[0]
    cpal = fileHead[1]
    imgs = fileHead[2]
    mask = fileHead[3]

    print("Header Type   :", hex(type))
    print("Color palette :", hex(cpal))

    fpos = srcfile.tell()

    mode_0 = False

    for img in range(imgs):
        imgHead = struct.unpack("<hhHHII",srcfile.read(16))
        xpos = imgHead[0]
        ypos = imgHead[1]
        wdth = imgHead[2]
        hght = imgHead[3]
        addr = imgHead[4]
        size = imgHead[5]
        unkn = srcfile.read(4)

        fpos = srcfile.tell()

        if img == 0 and type == 0 and addr != 0:
            print("[DEBUG] First address is not", hex(0), "but", hex(addr), end="")
            if addr == 8+imgs*20:
                print("; matches header size")
                print("[DEBUG] Switching to absolute position mode..." )
                mode_0 = True
            else:
                print()

        print("Frame", img+1, "of", imgs, "\tX: ", xpos, "Y: ", ypos, "   W: ", wdth, "H: ", hght)
        print("A: ", hex(addr), "(", hex(addr) if mode_0 else hex(addr + 8+imgs*20), ")", "S: ", size)

        header = BMPtoolkit._header

        header["width"] = wdth
        header["height"] = hght
        header["bitCount"] = 16

        # Jump to end of data to invert row order
        if mode_0 == False:
            bin = srcfile.seek(addr + 8+imgs*20 + size)
        else:
            bin = srcfile.seek(addr + size)

        pixels = b''

        for row in range(header['height']):
            srcfile.seek(srcfile.tell() - wdth * 2)
            pixels += srcfile.read(2*header['width'])
            pixels += BMPtoolkit.row_padding(header['width'], header['bitCount'])
            srcfile.seek(srcfile.tell() - wdth * 2)

        if imgs > 1:
            name = os.path.splitext(sys.argv[1+f])[0] + "__" + str(img) + ".bmp"
        else:
            name = os.path.splitext(sys.argv[1+f])[0] + ".bmp"

        BMPtoolkit.write(header, pixels, name)

        srcfile.seek(fpos)

    srcfile.close()
    print()
