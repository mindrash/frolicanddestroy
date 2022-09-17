count=1
timestamp=$(date +%s)
echo "removing files"
rm ./frames/*
echo "starting poc"
python3 poc.py
echo "starting convert"
convert -dispose background -layers OptimizeTransparency -delay 30 ./frames/*.png +repage -loop 0 "./out/fad-${timestamp}.gif"
#echo "starting mogrify"
#mogrify -layers 'optimize' -fuzz 10% "./out/fad-${timestamp}.gif"
#echo "starting resize 1"
#convert "./out/fad-${timestamp}.gif" -coalesce -resize 1350x1800 -layers optimize -loop 0 "./out/fad-${timestamp}-resize-1.gif"
echo "starting resize 2"
convert "./out/fad-${timestamp}.gif" -coalesce -resize 1080x1440 -layers optimize -loop 0 "./out/fad-${timestamp}-resize-2.gif"
