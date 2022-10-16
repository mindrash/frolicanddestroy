count=1

echo "starting gif making"

for d in */ ; do 
    echo "$d"
    [[ "$d" =~ "staged" ]] && continue
    timestamp=$(date +%s)
    seconds=$(date +%S)
    echo "seconds: $seconds"

    sq_count=$(find ./$d/square/*.png -type f | wc -l)
    rec_count=$(find ./$d/rectangle/*.png -type f | wc -l)
    echo "seconds: $seconds"

    if [ "$sq_count" -ge 8 ] && [ "$rec_count" -ge 8 ];
    then
        echo "$count processing $d"
        echo "starting sq convert"
        convert -dispose background -layers OptimizeTransparency -delay $seconds ./$d/square/*.png +repage -loop 0 "./$d/square/sq-${timestamp}.gif"
        echo "starting sq mogrify"
        mogrify -layers 'optimize' -fuzz 5% "./$d/square/sq-${timestamp}.gif"
        #echo "starting sq resize"
        #convert "./$d/square/sq-${timestamp}.gif" -coalesce -resize 1000x1000 -loop 0 "./$d/square/sq-1000x1000-${timestamp}.gif"

        echo "starting rc convert"
        convert -dispose background -layers OptimizeTransparency -delay $seconds ./$d/rectangle/*.png +repage -loop 0 "./$d/rectangle/rc-${timestamp}.gif"
        echo "starting rc mogrify"
        mogrify -layers 'optimize' -fuzz 5% "./$d/rectangle/rc-${timestamp}.gif"
        #echo "starting rc resize"
        #convert "./$d/rectangle/rc-${timestamp}.gif" -coalesce -resize 1000x1000 -loop 0 "./$d/rectangle/rc-1000x1000-${timestamp}.gif"
        count=count + 1
    else
        echo "skipping $d"
    fi

    mv ./$d "./staged-$d"
done
