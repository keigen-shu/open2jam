#!/usr/bin/env python3

import os, sys, struct

"""
O2Jam OPI Archive Extractor
Script by Keigen Shu

Main Header [16 bytes]
0x0 ~ 0x3 >> 02 00 00 00 (File identifier)
0x4 ~ 0x8 >> Number of files
0x8 ~ 0xF >> 00 00 00 00 00 00 00 00 (Unknown)

0xF ~ 0x? >> File data area                 [*1]
0x? ~ EOF >> File descriptors

File Descriptor [152 bytes for each file]
0x00 ~ 0x03 - File Status                   [*2]
0x04 ~ 0x84 - 128 bytes File Name in ASCII
0x84 ~ 0x87 - File Address (relative to beginning of OPI file)
0x88 ~ 0x8B - File Data Size ?
0x8C ~ 0x8F - File Data Area Size ?
0x90 ~ 0x97 - 00 00 00 00 00 00 00 00 (Unknown)

[1] Files are stored raw, uncompressed and unencrypted.
[2] 0 if file is hidden/removed. 1 if file is available.

"""


if len(sys.argv) < 2:
    sys.exit('Usage: %s OPI file to extract' % sys.argv[0])


if not os.path.exists(sys.argv[1]):
    sys.exit('ERROR: File %s was not found!' % sys.argv[1])
else:
    print("File:",sys.argv[1])

srcfile = open(sys.argv[1], "rb")

fileHead = struct.unpack("IIQ", srcfile.read(16))

fileID = fileHead[0]
files  = fileHead[1]
unkn   = filehead[2]

print("File ID   :", hex(fileID))
print("File count:", files)

if unkn != 0:
    print("[warn] Unusual file descriptor padding.")

srcfile.seek(0,2)
fend = srcfile.tell()

unkc = 0

for f in range(files):
    srcfile.seek(-152*(files-f),2)
    fileHead = struct.unpack("<I128sI2IQ",srcfile.read(152))
    head = fileHead[0]
    name = fileHead[1]
    addr = fileHead[2]
    siz1 = fileHead[3]
    siz2 = fileHead[4]
    unkn = fileHead[5]

    print(  "{:6}".format(f), "@", "0x{:08x}".format(addr), "+",
            "{:10} + {:10}".format(siz1, siz2-siz1), ":",
            "<unknown>" if head == 0 else "\"" + name.decode("ascii") + "\""
            )

    if unkn != 0:
        print("[warn] Unusual file descriptor padding.")

    srcfile.seek(addr,0)

    if head == 0:
        name = "unknown{}".format(unkc)
        outfile = open(name, "wb")
        outfile.write(srcfile.read(siz2))
        outfile.close()
    else:
        name = name.decode("ascii").rstrip('\0')
        outfile = open(name, "wb")
        outfile.write(srcfile.read(siz1))
        outfile.close()

srcfile.close()

print("Legend: File number @ Data Start Address + File Size + Free Area Available : \"File Name\"")
print()
