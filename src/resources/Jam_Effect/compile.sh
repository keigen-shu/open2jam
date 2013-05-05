#/bin/sh

a=1
while [ $a -lt 20 ]; do
    echo "Compiling Combo Text for arena $a ..."
    j=$(find Playing_Effect_Jam$((a))__*.bmp -type f | sort -t_ -n -k5,5 | xargs)
    montage $j -geometry +0+0 Playing_Effect_Jam$((a)).png
    a=$((a + 1))
done
