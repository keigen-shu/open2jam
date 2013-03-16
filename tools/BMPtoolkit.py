#!/usr/bin/env python3
import struct, random

_header = {
    'BM'          :b"BM",
                       # 2 bytes
    'sizeFile'    :0,  # 4 bytes
    'reserved'    :0,  # 2 + 2 bytes
    'offset'      :54, # 4 bytes

    'sizeHeader'  :40, # DIB Header = BITMAPINFOHEADER
    
    # BITMAPINFOHEADER
    'width'       :0,
    'height'      :0,
    'planes'      :1,
    'bitCount'    :24,
    'compression' :0,
    'sizeImage'   :0,
    'X_PPM'       :2835,
    'Y_PPM'       :2835,
    'clrUsed'     :0,
    'clrImportant':0
}

def write (header, pixels, filename):
    header["sizeImage"] = len(pixels)
    header["sizeFile"]  = header["sizeImage"] + header["sizeHeader"]
    
    header_str  = b""
    header_str += b'BM'
    header_str += struct.pack('<I', header['sizeFile'])
    header_str += struct.pack('<I', header['reserved'])
    header_str += struct.pack('<I', header['offset'])
    header_str += struct.pack('<I', header['sizeHeader'])
    header_str += struct.pack('<i', header['width'])
    header_str += struct.pack('<i', header['height'])
    header_str += struct.pack('<H', header['planes'])
    header_str += struct.pack('<H', header['bitCount'])
    header_str += struct.pack('<I', header['compression'])
    header_str += struct.pack('<I', header['sizeImage'])
    header_str += struct.pack('<i', header['X_PPM'])
    header_str += struct.pack('<i', header['Y_PPM'])
    header_str += struct.pack('<L', header['clrUsed'])
    header_str += struct.pack('<L', header['clrImportant'])

    #create the outfile
    outfile = open(filename, 'wb')
    
    #write the header + pixels
    outfile.write(header_str + pixels)
    outfile.close()

def row_padding(width, colordepth):
    byte_length = width * colordepth / 8
    # how many bytes are needed to make byte_length evenly divisible by 4?
    padding = int((4 - byte_length) % 4) 
    padbytes = b''
    for i in range(padding):
        x = struct.pack('<B',0)
        padbytes += x

    return padbytes
