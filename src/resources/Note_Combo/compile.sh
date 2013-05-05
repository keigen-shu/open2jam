#/bin/sh

a=1
while [ $a -lt 20 ]; do
    echo "Compiling Combo Text for arena $a ..."
    j=$(find Note_Combo$((a))__*.bmp -type f | sort -t_ -n -k5,5 | xargs)
    montage $j -geometry +0+0 Note_Combo$((a)).png
    a=$((a + 1))
done
