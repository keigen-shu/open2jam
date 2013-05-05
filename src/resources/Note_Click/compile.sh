#/bin/sh

a=1
while [ $a -lt 20 ]; do
    j=$(find Note_Click$((a))_1__*.bmp -type f | sort -t_ -n -k5,5 | xargs)
    montage $j -geometry +0+0 Note_Click$((a))_1.png
    j=$(find Note_Click$((a))_2__*.bmp -type f | sort -t_ -n -k5,5 | xargs)
    montage $j -geometry +0+0 Note_Click$((a))_2.png
    a=$((a + 1))
done
