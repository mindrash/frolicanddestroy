from random import randrange
from turtle import width
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageChops, ImageOps
from colorthief import ColorThief
import numpy as np
import cv2

def main():
    has_heart_beat = False
    is_inverted = False
    border_color = "#fffede"

    m1 = randrange(30, 57)
    print(f"First image is: {m1}")

    m2 = m1
    while m1 == m2:
        m2 = randrange(15, 43)

    print(f"Second image is: {m2}")

    m1_path = f'img/{m1}.png'
    m2_path = f'img/{m2}.png'

    im = Image.open(m1_path)
    if 1 == randrange(1, 4):
        im = im.convert("RGB")
        im = ImageOps.invert(im)

    im2 = Image.open(m2_path)
    if 1 == randrange(1, 4):
        im2 = im2.convert("RGB")
        im2 = ImageOps.invert(im2)

    im = im.convert("RGBA")
    im2 = im2.convert("RGBA")

    factor = randrange(3, 9)
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(factor)
    enhancer = ImageEnhance.Contrast(im2)
    im2 = enhancer.enhance(factor)

    datas = im.getdata()

    if 1 == randrange(1, 20):
        border_color = "#000000"

    frames = 6
    count = 2
    step = 30

    w, h = 5400, 7200
    border_width = 200
    shape = [(0, 0), (w, h)]
    im_rect = ImageDraw.Draw(im)
    im_rect.rectangle(shape, outline=border_color, width=border_width, fill=None)
  
    str_c = str(count - 1)
    if len(str_c) == 1:
        str_c = "0" + str_c

    im.save(f"frames/fad-{str_c}.png")
    stop_color = randrange(255, 256)
    color_value = stop_color

    rotate = 1

    stop_color2 = step
    step2 = 15

    high_low = randrange(0, 4)

    while count <= frames:
        what_color = randrange(0, 3)
        im3 = im2
        im_working = im

        new_image_data = []
        if high_low:
            for item in datas:
                if (item[what_color] in list(range(color_value, stop_color))):
                    new_image_data.append((255, 255, 255, 0))
                else:
                    new_image_data.append(item)
                    
        else:
            for item in datas:
                if (item[0] in list(range(0, stop_color2))):
                    new_image_data.append((255, 255, 255, 0))
                else:
                    new_image_data.append(item)

        im_working.putdata(new_image_data) 
        im_working = im_working.convert("RGBA")

        #datas = im_working.getdata()
    
        #newData = []
    
        #for item in datas:
        #    if item[0] == 255 and item[1] == 255 and item[2] == 255:
        #        newData.append((255, 255, 255, 0))
        #    else:
        #        newData.append(item)
    
        #im_working.putdata(newData)

        #enhancer = ImageEnhance.Contrast(im3)
        #im3 = enhancer.enhance(factor)

        x = 0
        y = 0
        beat_size = randrange(10, 100)

        if rotate == 2:
            x = 0
            y = 0
            im3 = im3.resize((w + beat_size, h + beat_size))
            rotate += 1
            print("rotate")
        elif rotate == 3:
            x = 0
            y = 0
            rotate += 1
        elif rotate == 4:
            x = 0
            y = 0
            im3 = im3.resize((w + beat_size, h + beat_size))
            rotate = 1
        else:
            rotate += 1

        im3.paste(im_working, (x,y), mask=im_working)

        im_rect = ImageDraw.Draw(im3)
        im_rect.rectangle(shape, outline=border_color, width=200, fill=None)

        str_c1 = str(count)
        if len(str_c1) == 1:
            str_c1 = "0" + str_c1

        im2.save(f"frames/fad-{str_c1}.png")

        str_c2 = str((frames * 2) - (count - 1))
        if len(str_c2) == 1:
            str_c2 = "0" + str_c2

        im2.save(f"frames/fad-{str_c2}.png")
        color_value -= step
        stop_color2 += step2
        count += 1

if __name__ == "__main__":
    main()