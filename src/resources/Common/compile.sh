#/bin/sh

echo "Compiling Long Note Effect..."
j=$(find LongNote_Effect__*.bmp -type f | sort -t_ -n -k5,5 | xargs)
montage $j -geometry +0+0 LongNote_Effect.png

echo "Compiling LX#.# sprites..."
j=$(find main_level__*.bmp -type f | sort -t_ -n -k5,5 | xargs)
montage $j -geometry +0+0 main_level.png

echo "Compiling Jam Level counter numbers and text..."
j=$(find Note_Jam__*.bmp -type f | sort -t_ -n -k5,5 | xargs)
montage $j -geometry '1x1+0+0<' Note_Jam.png
j=$(find Note_JamNum__*.bmp -type f | sort -t_ -n -k5,5 | xargs)
montage $j -geometry '1x1+0+0<' Note_JamNum.png

echo "Compiling Exit button..."
montage Playing_Exit__0.bmp Playing_Exit__1.bmp -geometry +0+0 Playing_Exit.png

echo "Done. Please do the rest of the work with an image editor like GIMP."
