from random import randrange
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageChops, ImageOps
from os import listdir
from os.path import isfile, join
from glitch_this import ImageGlitcher
import time
import datetime
import json
import random
import torchvision.transforms.functional as F
import pyfiglet
import logging
import os
import glob

def main():
    name = "Regret This Purchase"
    description = "A generative art collection by mindrash began as a follow up to Frolic and Detour. The lineage continues to explore the legal concept as a metaphor in life together with the journey through this technology stack. It incorporates heightened movement as breath and heartbeat that can be experienced with the risk, reward, and failure in this space. Randomness dominates but is framed with constraints. There is an exterior and an interior to each piece with palettes mixing and eroding between."

    print(pyfiglet.figlet_format(name))
    print("Starting: " + str(datetime.datetime.now()))
    logging.basicConfig(level=logging.INFO, filename='logs/app-1.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    logging.info(pyfiglet.figlet_format(name))
    console_line = "*" * 80
    print(console_line)
    logging.info(console_line)
    logging.info("Starting: " + str(datetime.datetime.now()))

    mypath = "img/"
    mypath_txt = "img_txt/"
    metapath = "meta/"

    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    files.sort()
    max_total = 999
    total = 0

    for file in files:
        current_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        if len(current_files) < 2:
            print("not enough files")
            break
        current_file1 = current_files[0]
        current_file2 = current_files[1]

        if ".png" not in current_file1 or not os.path.isfile(mypath + current_file1):
            print("no pngs")
            continue

        base_filename = current_file1.replace(".png", ".txt")
        with open(f"{mypath_txt}{base_filename}", "r") as txt_file:
            txt_info = txt_file.readline().split(",")

        generations = txt_info[0]
        all_palettes = txt_info[1]

        sq_or_rect = "square"
        has_heart_beat = True
        is_inverted = False
        special_border = False
        has_trip = False
        has_glitch = False
        has_section_glitch = False
        has_section_frame = False
        is_black_and_white = False
        num_lines = 3

        border_width = 200
        border_color = "#fffede"

        try:
            ts = round(time.time())
            directory = str(ts)
            parent_dir = "./out"
            path = os.path.join(parent_dir, directory)
            os.mkdir(path)
            print("Directory '%s' created" %directory)
            path_sq = path + "/square"
            os.mkdir(path_sq)
            path_rect = path + "/rectangle"
            os.mkdir(path_rect)
            use_path = path_sq

            logging.info(f"Creating: {ts} {str(datetime.datetime.now())}")
            if total > max_total:
                break

            for shape_count in range(0, 2):
                if shape_count == 1:
                    sq_or_rect = "rectangle"
                    use_path = path_rect

                if 1 == randrange(1, 6):
                    special_border = True
                    print(f"special_border: {special_border}")
                    has_trip = True
                    print(f"has_trip: {has_trip}")

                if 1 == randrange(1, 20):
                    border_color = "#202020"

                frames = randrange(4, 9)
                print(f"frames: {frames}")
                count = 1
                step = round(255 / frames)

                top = current_file1
                print(f"First image is: {top}")

                bottom = current_file2

                print(f"Second image is: {bottom}")

                top_path = f'img/{top}'
                bottom_path = f'img/{bottom}'

                top_img = Image.open(top_path)
                top_img = make_sq_or_rect(sq_or_rect, top_img)

                w, h = top_img.size

                if 1 == randrange(0, 4):
                    top_img = top_img.convert("RGB")
                    top_img = ImageOps.invert(top_img)
                    is_inverted = True
                    print(f"is_inverted: {is_inverted}")
            
                bottom_img = Image.open(bottom_path)
                bottom_img = make_sq_or_rect(sq_or_rect, bottom_img)

                if 1 == randrange(0, 4):
                    bottom_img = bottom_img.convert("RGB")
                    bottom_img = ImageOps.invert(bottom_img)
                    is_inverted = True
                    print(f"is_inverted: {is_inverted}")

                factor = randrange(1, 50)
                print(f"Factor: {factor}")
                enhancer = ImageEnhance.Contrast(bottom_img)
                bottom_img = enhancer.enhance(factor)
                enhancer = ImageEnhance.Contrast(top_img)
                top_img = enhancer.enhance(factor)

                if 1 == randrange(1, 20):
                    has_glitch = True
                    glitcher = ImageGlitcher()
                    top_img = glitcher.glitch_image(top_img, randrange(1, 3), color_offset=False)
                    bottom_img = glitcher.glitch_image(bottom_img, randrange(1, 3), color_offset=False)

                border_size = 5
                x1_section = 0
                y1_section = 0
                x2_section = 0
                y2_section = 0
                frame_size = 0

                if 1 == randrange(1, 5) and not has_trip and not has_glitch:            
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
                    if 1 == randrange(0, 2):
                        bottom_img_section = bottom_img_section.convert("RGB")
                        top_img_section = top_img_section.convert("RGB")
                        top_img_section = ImageOps.invert(top_img_section)
                        bottom_img_section = ImageOps.invert(bottom_img_section)
                        bottom_img = bottom_img.convert("RGBA")
                        top_img = top_img.convert("RGBA")
                    top_img_section = glitcher.glitch_image(top_img_section, randrange(1, 3), color_offset=False)
                    bottom_img_section = glitcher.glitch_image(bottom_img_section, randrange(1, 3), color_offset=False)
                    top_img_section = top_img_section.convert("RGBA")
                    bottom_img_section = bottom_img_section.convert("RGBA")
                    top_img.paste(top_img_section, (x1_section, y1_section), top_img_section)        
                    bottom_img.paste(bottom_img_section, (x1_section, y1_section), bottom_img_section)
                    im_rect = ImageDraw.Draw(top_img)
                    im_rect.rectangle((x1_section - border_width/2, y1_section - border_width/2, x2_section + border_width/2, y2_section + border_width/2,), outline=border_color, width=border_width, fill=None)
                    im_rect = ImageDraw.Draw(bottom_img)
                    im_rect.rectangle((x1_section - border_width/2, y1_section - border_width/2, x2_section + border_width/2, y2_section + border_width/2,), outline=border_color, width=border_width, fill=None)

                    if has_section_frame:
                        frame_size = border_width
                        print(f"frame_size: {frame_size}")
                        add_frame(w, h, border_color, bottom_img, x1_section, y1_section, x2_section, y2_section, frame_size)
                        add_frame(w, h, border_color, top_img, x1_section, y1_section, x2_section, y2_section, frame_size)
                elif has_trip:
                    top_img, bottom_img = trip_glitch(w, h, top_img, bottom_img)

                if 1 == randrange(1, 4):
                    is_black_and_white = True
                    border_color = "#ffffff"
                    factor = randrange(5, 20)
                    if 1 == randrange(1, 3):
                        top_img = ImageOps.grayscale(top_img)
                        enhancer = ImageEnhance.Contrast(top_img)
                        top_img = enhancer.enhance(factor)
                    bottom_img = ImageOps.grayscale(bottom_img)
                    enhancer = ImageEnhance.Contrast(bottom_img)
                    bottom_img = enhancer.enhance(factor)

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

                im_rect = ImageDraw.Draw(top_img)
                im_rect.rectangle(shape, outline=border_color, width=border_width, fill=None)

                final_border(1, border_color, top_img, shape)

                make_tri(top_img)

                top_img.save(f"{use_path}/{ts}-{sq_or_rect}-{str_c}.png")

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
                        top_img_out = glitcher.glitch_image(top_img_out, randrange(1, 6), color_offset=False)
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

                    if has_section_glitch and not has_trip:
                        print(f"has_section_glitch: {has_section_glitch}")
                        glitcher = ImageGlitcher()
                        section_shape = (x1_section, y1_section, x2_section, y2_section)
                        top_img_section = top_img_out.crop(section_shape)
                        bottom_img_section = bottom_img_out.crop(section_shape)
                        top_img_section = glitcher.glitch_image(top_img_section, randrange(1, 3), color_offset=False)
                        bottom_img_section = glitcher.glitch_image(bottom_img_section, randrange(1, 3), color_offset=False)
                        top_img_section = top_img_section.convert("RGBA")
                        bottom_img_section = bottom_img_section.convert("RGBA")
                        top_img_out.paste(top_img_section, (x1_section, y1_section), top_img_section)        
                        bottom_img_out.paste(bottom_img_section, (x1_section, y1_section), bottom_img_section)
                        im_rect = ImageDraw.Draw(top_img_out)
                        im_rect.rectangle((x1_section - border_width/2, y1_section - border_width/2, x2_section + border_width/2, y2_section + border_width/2,), outline=border_color, width=border_width, fill=None)
                        im_rect = ImageDraw.Draw(bottom_img_out)
                        im_rect.rectangle((x1_section - border_width/2, y1_section - border_width/2, x2_section + border_width/2, y2_section + border_width/2,), outline=border_color, width=border_width, fill=None)
                    elif has_trip:
                        top_img_out, bottom_img_out = trip_glitch(w, h, top_img, bottom_img)

                    x = 0
                    y = 0

                    if has_heart_beat:
                        beat_size = randrange(0, 20)
                        if not special_border:
                            beat_size = randrange(0, 20)

                        print(f"beat_size: {beat_size}")

                        if heartbeat == 2:
                            x = 0
                            y = 0
                            bottom_img_out = bottom_img_out.resize((w + beat_size, h + beat_size)).crop((0,0,w,h))
                            top_img_out = top_img_out.resize((w + beat_size, h + beat_size)).crop((0,0,w,h))
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
                    
                    bottom_img_out.paste(top_img_out, (0,0), mask=top_img_out)
                    if count > 2:
                        bottom_img_out = F.adjust_hue(bottom_img_out, random.uniform(-.1, .1))

                    final_border(2, border_color, bottom_img_out, shape)
                    make_tri(bottom_img_out)

                    final = Image.new(size=(w, h), color=border_color, mode="RGBA")
                    final.paste(bottom_img_out, (0, 0), bottom_img_out)

                    str_c1 = str(count)
                    if len(str_c1) == 1:
                        str_c1 = "0" + str_c1

                    final.save(f"{use_path}/{ts}-{sq_or_rect}-{str_c1}.png")

                    str_c2 = str((frames * 2) - (count - 1))
                    if len(str_c2) == 1:
                        str_c2 = "0" + str_c2

                    final.save(f"{use_path}/{ts}-{sq_or_rect}-{str_c2}.png")            

                    if color_value < step:
                        color_value = 0
                    else:
                        color_value -= step

                    data_name = f"{ts}-{sq_or_rect}.json"
                    name = ""
                    if "square" in sq_or_rect:
                        name = "Square"
                    else:
                        name = "Rectangle"

                    ipfs_url = "ipfs://[[IPFS_URL]]"
                    nft_json = {
                        "description" : description,
                        "external_url" : "https://mindrash.com/regret-this-purchase.html",
                        "image" : ipfs_url,
                        "name" : f"Regret This {name}: [[token_id]]",
                        "attributes" : [
                            {
                                "trait_type" : "is_sq_or_rect",
                                "value" : sq_or_rect
                            },
                            {
                                "trait_type" : "1000x1000_ipfs",
                                "value" : "ipfs://[[1000x1000_ipfs]]"
                            },
                            {
                                "trait_type" : "has_triptych",
                                "value" : str(has_trip)
                            },
                            {
                                "trait_type" : "has_section_frame",
                                "value" : str(has_section_frame)
                            },
                            {
                                "trait_type" : "has_glitch",
                                "value" : str(has_glitch)
                            },
                            {
                                "trait_type" : "is_inverted",
                                "value" : str(is_inverted)
                            },
                            {
                                "trait_type" : "is_black_and_white",
                                "value" : str(is_black_and_white)
                            },
                            {
                                "trait_type" : "border_color",
                                "value" : border_color
                            },
                            {
                                "trait_type" : "frame_count",
                                "value" : str(frames)
                            },
                            {
                                "trait_type" : "generations",
                                "value" : generations
                            },
                            {
                                "trait_type" : "all_palettes",
                                "value" : all_palettes
                            },
                            {
                                "trait_type" : "layer1",
                                "value" : top_path
                            },
                            {
                                "trait_type" : "layer2",
                                "value" : bottom_path
                            },
                        ],
                    }

                    with open(metapath + data_name, "w") as data_file:
                        json.dump(nft_json, data_file)
                        data_file.close()

                    count += 1
                total += 1

            logging.info(f"{ts}: {nft_json}")

            if shape_count == 1:
                os.rename(top_path, top_path.replace("img", "processed"))
                os.rename(bottom_path, bottom_path.replace("img", "processed"))

        except Exception as ex:
            print(ex)
            logging.info(f"{ex}")


def make_sq_or_rect(sq_or_rect, top_img):
    if sq_or_rect == "square":
        top_img = top_img.resize((6000,6000))
    else:
        top_img = top_img.crop((0,0,5400, 7200))
    return top_img

def final_border(border_width, border_color, top_img, shape):
    if border_color == "#202020":
        border_color = "#fffede"
    else:
        border_color = "#202020"
    
    im_rect = ImageDraw.Draw(top_img)
    im_rect.rectangle(shape, outline=border_color, width=border_width, fill=None)

def trip_glitch(w, h, top_img, bottom_img):
    print("making trip_glitch")
    offset = 200
    glitcher = ImageGlitcher()
    top_img_section = top_img.crop((0, round(h * .33) + offset, w, round(h * .66) + offset))
    bottom_img_section = bottom_img.crop((0, round(h * .33) + offset, w, round(h * .66) + offset))
    top_img_section = glitcher.glitch_image(top_img_section, randrange(1, 3), color_offset=False)
    bottom_img_section = glitcher.glitch_image(bottom_img_section, randrange(1, 3), color_offset=False)
    top_img_section = top_img_section.convert("RGBA")
    bottom_img_section = bottom_img_section.convert("RGBA")
    top_img.paste(top_img_section, (0, round(h * .33) + offset), top_img_section)        
    bottom_img.paste(bottom_img_section, (0, round(h * .33) + offset), bottom_img_section)
    return top_img, bottom_img

def make_tri(top_img):
    triangle = ImageDraw.Draw(top_img)
    triangle.polygon([(50, 50), (50, 250), (250, 50) ], fill="#FF8200")

def make_glow_ring(w, h, border_width, top_img):
    glow_ring = Image.new('RGBA', (w, h), (255, 0, 0, 0))
    glow_rect = ImageDraw.Draw(glow_ring)
    glow_color = "#8A026A"
    glow_shape = [(border_width, border_width), (w - border_width, h - border_width)]
    glow_width = 25
    glow_rect.rectangle(glow_shape, outline=glow_color, width=glow_width, fill=None)
    glow_ring = glow_ring.filter(ImageFilter.GaussianBlur(radius = 50))
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