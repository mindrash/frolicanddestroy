from random import randrange
from turtle import width
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageChops, ImageOps
from colorthief import ColorThief
import numpy as np
import cv2
from os import listdir
from os.path import isfile, join

def main():
    has_heart_beat = False
    is_inverted = False
    border_color = "#fffede"
    mypath = "img/"

    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    files.sort(reverse=True)
    total = 0

    for file in files:
        if total > 0:
            break

        m1 = file
        print(f"First image is: {m1}")

        m2 = m1
        while m1 == m2:
            m2 = files[randrange(len(files))]

        print(f"Second image is: {m2}")

        m1_path = f'img/{m1}'
        m2_path = f'img/{m2}'

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
        print(f"Factor: {factor}")
        enhancer = ImageEnhance.Contrast(im)
        im = enhancer.enhance(factor)
        enhancer = ImageEnhance.Contrast(im2)
        im2 = enhancer.enhance(factor)

        datas = im.getdata()

        if 1 == randrange(1, 20):
            border_color = "#000000"

        frames = 8
        count = 1
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
        stop_color = randrange(245, 256)
        color_value = stop_color

        heartbeat = 1
        print(f"heartbeat: {heartbeat}")

        stop_color2 = step
        step2 = 5

        high_low = randrange(0, 4)
        print(f"high_low: {high_low}")
        throttle = True
        what_color = randrange(0, 3)

        while count <= frames:
            print(f"Starting frame: {count}")
            im3 = im2
            im_working = im

            new_image_data = []
            for item in datas:
                if (item[what_color] in list(range(color_value, stop_color))):
                    new_image_data.append((255, 255, 255))
                else:
                    new_image_data.append(item)
                        
            im_working.putdata(new_image_data) 

            if high_low == 0:
                new_image_data = []
                for item in datas:
                    if (item[what_color] in list(range(0, stop_color2))):
                        new_image_data.append((255, 255, 255))
                        throttle = False
                    else:
                        new_image_data.append(item)
                im_working.putdata(new_image_data) 
    
            im_working = im_working.convert("RGBA")

            pixdata = im_working.load()

            for y in range(h):
                for x in range(w):
                    if pixdata[x, y] == (255, 255, 255, 255):
                        pixdata[x, y] = (255, 255, 255, 0)

            x = 0
            y = 0
            beat_size = randrange(10, 100)

            if heartbeat == 2:
                x = 0
                y = 0
                im3 = im3.resize((w + beat_size, h + beat_size))
                heartbeat += 1
            elif heartbeat == 3:
                x = 0
                y = 0
                heartbeat += 1
            elif heartbeat == 4:
                x = 0
                y = 0
                im3 = im3.resize((w + beat_size, h + beat_size))
                heartbeat = 1
            else:
                heartbeat += 1

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
            if throttle:
                step *= 2
            color_value -= step
            stop_color2 += step2
            count += 1
            total += 1

if __name__ == "__main__":
    main()