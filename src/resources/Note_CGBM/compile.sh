#!/bin/sh


i=1
while [ $i -lt 20 ]; do
    echo "Compiling COOL, GOOD, BAD and MISS text for arena $i ..."
    montage Note_Miss$((i)).bmp Note_Bad$((i)).bmp Note_Good$((i)).bmp Note_Cool$((i)).bmp -geometry +0+0 Note_CGBM$((i)).png
    i=$((i + 1))
done
