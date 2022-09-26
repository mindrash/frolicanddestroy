from random import randrange
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageChops, ImageOps
from os import listdir
from os.path import isfile, join
from glitch_this import ImageGlitcher

def main():
    has_heart_beat = True
    is_inverted = False
    special_border = False
    has_horizon_lines = False
    has_trip = False
    has_glitch = False
    has_section_glitch = False
    has_section_frame = False

    w, h = 6000, 6000
    border_width = 200
    border_color = "#fffede"
    mypath = "img/"

    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    files.sort()
    total = 0

    for file in files:
        if total > 0:
            break

        num_lines = 0

        if 1 == randrange(1, 6):
            special_border = True
            print(f"special_border: {special_border}")
            has_trip = True
            num_lines = randrange(3, 4)
            print(f"num_lines: {num_lines}")
            print(f"has_trip: {has_trip}")

        if 1 == randrange(1, 20):
            border_color = "#202020"

        frames = randrange(4, 9)
        print(f"frames: {frames}")
        count = 1
        step = round(255 / frames)

        top = file
        print(f"First image is: {top}")

        bottom = top
        while bottom == top:
            bottom = files[randrange(len(files))]

        print(f"Second image is: {bottom}")

        top_path = f'img/{top}'
        bottom_path = f'img/{bottom}'

        top_img = Image.open(top_path)
        if 1 == randrange(0, 4):
            top_img = top_img.convert("RGB")
            top_img = ImageOps.invert(top_img)
            is_inverted = True
            print(f"is_inverted: {is_inverted}")
      
        bottom_img = Image.open(bottom_path)
        if 1 == randrange(0, 4):
            bottom_img = bottom_img.convert("RGB")
            bottom_img = ImageOps.invert(bottom_img)
            is_inverted = True
            print(f"is_inverted: {is_inverted}")

        factor = randrange(3, 19)
        print(f"Factor: {factor}")
        enhancer = ImageEnhance.Contrast(bottom_img)
        bottom_img = enhancer.enhance(factor)
        enhancer = ImageEnhance.Contrast(top_img)
        top_img = enhancer.enhance(factor)

        if 1 == randrange(1, 20):
            has_glitch = True
            glitcher = ImageGlitcher()
            top_img = glitcher.glitch_image(top_img, randrange(1, 11), color_offset=True)
            bottom_img = glitcher.glitch_image(bottom_img, randrange(1, 11), color_offset=True)

        border_size = 5
        x1_section = 0
        y1_section = 0
        x2_section = 0
        y2_section = 0
        frame_size = 0

        if 1 == randrange(1, 3) and not has_trip:            
            has_section_glitch = True
            special_border = True
            border_size = border_width
            print(f"has_section_glitch: {has_section_glitch}")

            frame_min_dist = 500
            meets_min_dist = (x2_section < w - frame_min_dist and x1_section > w + frame_min_dist and y2_section < h - frame_min_dist and y1_section > h + frame_min_dist)
            print(f"meets_min_dist: {meets_min_dist}")
            if  1 == randrange(1, 3):
                has_section_frame = True
                border_size = 0

            glitch_border_color = border_color
            glitcher = ImageGlitcher()
            x1_section = randrange(1000, w - 2000)
            y1_section = randrange(1000, h - 2000)
            x2_section = x1_section + randrange(1000, 2000)
            y2_section = y1_section + randrange(1000, 2000)
            top_img_section = top_img.crop((x1_section, y1_section, x2_section, y2_section))
            bottom_img_section = bottom_img.crop((x1_section, y1_section, x2_section, y2_section))
            if 1 == randrange(1, 2):
                bottom_img_section = bottom_img_section.convert("RGB")
                top_img_section = top_img_section.convert("RGB")
                top_img_section = ImageOps.invert(top_img_section)
                bottom_img_section = ImageOps.invert(bottom_img_section)
                bottom_img = bottom_img.convert("RGBA")
                top_img = top_img.convert("RGBA")
            top_img_section = ImageOps.expand(glitcher.glitch_image(top_img_section, randrange(1, 11), color_offset=True), border=border_size, fill=glitch_border_color)
            bottom_img_section = ImageOps.expand(glitcher.glitch_image(bottom_img_section, randrange(1, 11), color_offset=True), border=border_size, fill=glitch_border_color)
            top_img_section = top_img_section.convert("RGBA")
            bottom_img_section = bottom_img_section.convert("RGBA")
            top_img.paste(top_img_section, (x1_section, y1_section), top_img_section)        
            bottom_img.paste(bottom_img_section, (x1_section, y1_section), bottom_img_section)

            if has_section_frame:
                frame_size = border_width
                add_frame(w, h, border_color, bottom_img, x1_section, y1_section, x2_section, y2_section, frame_size)
                add_frame(w, h, border_color, top_img, x1_section, y1_section, x2_section, y2_section, frame_size)
        elif has_trip:
            trip_glitch(w, h, top_img, bottom_img)

        top_img = top_img.convert("RGBA")
        bottom_img = bottom_img.convert("RGBA")
        pass_img = top_img

        print(f"border_color: {border_color}")

        im_rect = ImageDraw.Draw(top_img)
    
        str_c = str(count - 1)
        if len(str_c) == 1:
            str_c = "0" + str_c

        shape = [(0, 0), (w, h)]

        if has_trip:
            im_rect = ImageDraw.Draw(top_img)
            print(f"has_trip: {has_trip}")
            for x in range(num_lines + 1):
                hmul = x/num_lines
                h1 = h * hmul
                h2 = h * hmul + border_width
                lshape = [(0, h1), (w, h2)]
                im_rect.rectangle(lshape, outline=border_color, width=border_width, fill=border_color)

        if not special_border and not has_glitch and not has_trip:
            make_glow_ring(w, h, border_width, top_img)

        im_rect = ImageDraw.Draw(top_img)
        im_rect.rectangle(shape, outline=border_color, width=border_width, fill=None)

        final_border(1, border_color, top_img, shape)

        make_tri(top_img)

        top_img.save(f"frames/fad-{str_c}.png")

        color_value = randrange(245, 256)

        heartbeat = 1
        print(f"heartbeat: {heartbeat}")

        if 1 == randrange(0, 2):
            has_heart_beat = True

        top_img_out = pass_img

        while count <= frames:
            print(f"Starting frame: {count}")
            print(f"color_value: {color_value}")
            bottom_img_out = bottom_img

            if special_border:
                top_img_out = pass_img

            if has_glitch and 1 == randrange(0, 2):
                top_img_out = glitcher.glitch_image(top_img_out, 10, color_offset=True)
                top_img_out = top_img_out.convert("RGBA")

            datas = top_img_out.getdata()
            newData = []
            for item in datas:
                if count == frames - 1:
                    if item[0] > color_value and item[1] > color_value or item[2] > color_value:
                        newData.append((255, 255, 255, 0))
                    else:
                        newData.append(item)
                else:
                    if 1 == randrange(0, 2):
                        if item[0] > color_value or (item[1] > color_value and item[2] > color_value):
                            newData.append((255, 255, 255, 0))
                        else:
                            newData.append(item)
                    else:
                        if item[0] > color_value and item[1] > color_value and item[2] > color_value:
                            newData.append((255, 255, 255, 0))
                        else:
                            newData.append(item)

            top_img_out.putdata(newData)

            enhancer = ImageEnhance.Contrast(bottom_img)
            factor += 1
            bottom_img = enhancer.enhance(factor)

            x = 0
            y = 0

            if has_heart_beat:
                beat_size = randrange(-20, 20)
                print(f"beat_size: {beat_size}")

                if heartbeat == 2:
                    x = 0
                    y = 0
                    bottom_img_out = bottom_img_out.resize((w + beat_size, h + beat_size)).crop((0,0,w,h))
                    heartbeat += 1
                elif heartbeat == 3:
                    x = 0
                    y = 0
                    heartbeat += 1
                elif heartbeat == 4:
                    x = 0
                    y = 0
                    bottom_img_out = bottom_img_out.resize((w + beat_size, h + beat_size)).crop((0,0,w,h))
                    heartbeat = 1
                else:
                    heartbeat += 1

            if has_section_glitch and not has_trip:
                print(f"has_section_glitch: {has_section_glitch}")
                glitcher = ImageGlitcher()
                top_img_section = top_img_out.crop((x1_section, y1_section, x2_section, y2_section))
                bottom_img_section = bottom_img_out.crop((x1_section, y1_section, x2_section, y2_section))
                if 1 == randrange(1, 2):
                    bottom_img_section = bottom_img_section.convert("RGB")
                    top_img_section = top_img_section.convert("RGB")
                    top_img_section = ImageOps.invert(top_img_section)
                    bottom_img_section = ImageOps.invert(bottom_img_section)
                    bottom_img = bottom_img.convert("RGBA")
                    top_img = top_img.convert("RGBA")
                top_img_section = ImageOps.expand(glitcher.glitch_image(top_img_section, randrange(1, 11), color_offset=True), border=border_size, fill=glitch_border_color)
                bottom_img_section = ImageOps.expand(glitcher.glitch_image(bottom_img_section, randrange(1, 11), color_offset=True), border=border_size, fill=glitch_border_color)
                top_img_section = top_img_section.convert("RGBA")
                bottom_img_section = bottom_img_section.convert("RGBA")
                top_img.paste(top_img_section, (x1_section, y1_section), top_img_section)        
                bottom_img.paste(bottom_img_section, (x1_section, y1_section), bottom_img_section)
            elif has_trip:
                trip_glitch(w, h, top_img, bottom_img)

            if has_section_frame:
                add_frame(w, h, border_color, top_img_out, x1_section, y1_section, x2_section, y2_section, frame_size)

            im_rect = ImageDraw.Draw(top_img_out)

            if special_border:
                if has_trip:
                    for x in range(num_lines + 1):
                        hmul = x/num_lines
                        h1 = h * hmul
                        h2 = h * hmul + border_width
                        lshape = [(0, h1), (w, h2)]
                        im_rect.rectangle(lshape, outline=border_color, width=border_width, fill=border_color)


            im_rect.rectangle(shape, outline=border_color, width=border_width, fill=None)

            if not special_border and not has_glitch and not has_trip:
                make_glow_ring(w, h, border_width, bottom_img_out)
            
            bottom_img_out.paste(top_img_out, (0,0), mask=top_img_out)
            make_tri(bottom_img_out)

            final_border(1, border_color, bottom_img_out, shape)

            str_c1 = str(count)
            if len(str_c1) == 1:
                str_c1 = "0" + str_c1

            bottom_img_out.save(f"frames/fad-{str_c1}.png")

            str_c2 = str((frames * 2) - (count - 1))
            if len(str_c2) == 1:
                str_c2 = "0" + str_c2

            bottom_img_out.save(f"frames/fad-{str_c2}.png")
            
            if color_value < step:
                color_value = 0
            else:
                color_value -= step
            
            count += 1
            total += 1

def final_border(border_width, border_color, top_img, shape):
    if border_color == "#202020":
        border_color = "#fffede"
    else:
        border_color = "#202020"
    
    im_rect = ImageDraw.Draw(top_img)
    im_rect.rectangle(shape, outline=border_color, width=border_width, fill=None)

def trip_glitch(w, h, top_img, bottom_img):
    print("making trip_glitch")
    glitcher = ImageGlitcher()
    top_img_section = top_img.crop((0, h * .33, w, h * .67))
    bottom_img_section = bottom_img.crop((0, h * .33, w, h * .67))
    if 1 == randrange(1, 2):
        bottom_img_section = bottom_img_section.convert("RGB")
        top_img_section = top_img_section.convert("RGB")
        top_img_section = ImageOps.invert(top_img_section)
        bottom_img_section = ImageOps.invert(bottom_img_section)
        bottom_img = bottom_img.convert("RGBA")
        top_img = top_img.convert("RGBA")
    top_img_section = glitcher.glitch_image(top_img_section, randrange(1, 11), color_offset=True)
    bottom_img_section = glitcher.glitch_image(bottom_img_section, randrange(1, 11), color_offset=True)
    top_img_section = top_img_section.convert("RGBA")
    bottom_img_section = bottom_img_section.convert("RGBA")
    top_img.paste(top_img_section, (0, round(h * .33)), top_img_section)        
    bottom_img.paste(bottom_img_section, (w, round(h * .67)), bottom_img_section)

def make_tri(top_img):
    triangle = ImageDraw.Draw(top_img)
    triangle.polygon([(50, 50), (50, 250), (250, 50) ], fill="#FF8200")

def make_glow_ring(w, h, border_width, top_img):
    glow_ring = Image.new('RGBA', (w, h), (255, 0, 0, 0))
    glow_rect = ImageDraw.Draw(glow_ring)
    glow_color = "#8A026A"
    glow_shape = [(border_width, border_width), (w - border_width, h - border_width)]
    glow_width = 50
    glow_rect.rectangle(glow_shape, outline=glow_color, width=glow_width, fill=None)
    glow_ring = glow_ring.filter(ImageFilter.GaussianBlur(radius = 25))
    top_img.paste(glow_ring, (0,0), glow_ring)

def add_frame(w, h, border_color, bottom_img, x1_section, y1_section, x2_section, y2_section, frame_size):
    img_line = ImageDraw.Draw(bottom_img)
    frame_shape = [(x1_section, 0), (x1_section, h)]
    img_line.line(frame_shape, fill=border_color, width=frame_size)
    frame_shape = [(x2_section, 0), (x2_section, h)]
    img_line.line(frame_shape, fill=border_color, width=frame_size)
    frame_shape = [(0, y1_section), (w, y1_section)]
    img_line.line(frame_shape, fill=border_color, width=frame_size)
    frame_shape = [(0, y2_section), (w, y2_section)]
    img_line.line(frame_shape, fill=border_color, width=frame_size)

if __name__ == "__main__":
    main()