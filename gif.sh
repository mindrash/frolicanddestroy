count=1

echo "starting poc"

for d in */ ; do 
    echo "$d"
    [[ "$d" =~ "staged" ]] && continue
    timestamp=$(date +%s)
    seconds=$(date +%S)

    #if [[ $seconds < 24 ]]
    #then
    #    seconds=seconds + 20
    #fi

    echo "seconds: $seconds"

    echo "starting sq convert"
    convert -dispose background -layers OptimizeTransparency -delay $seconds ./$d/square/*.png +repage -loop 0 "./$d/square/sq-${timestamp}.gif"
    echo "starting sq mogrify"
    #mogrify -layers 'optimize' -fuzz 1% "./out/fad-${timestamp}.gif"
    echo "starting sq resize"
    convert "./$d/square/sq-${timestamp}.gif" -coalesce -resize 1000x1000 -layers optimize -loop 0 "./$d/square/sq-1000x1000-${timestamp}.gif"

    echo "starting rc convert"
    convert -dispose background -layers OptimizeTransparency -delay $seconds ./$d/rectangle/*.png +repage -loop 0 "./$d/rectangle/rc-${timestamp}.gif"
    echo "starting rc mogrify"
    #mogrify -layers 'optimize' -fuzz 1% "./out/fad-${timestamp}.gif"
    echo "starting rc resize"
    convert "./$d/rectangle/rc-${timestamp}.gif" -coalesce -resize 1000x1000 -layers optimize -loop 0 "./$d/rectangle/rc-1000x1000-${timestamp}.gif"

    mv ./$d "./staged-$d"
done
