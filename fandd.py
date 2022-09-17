from PIL import Image, ImageEnhance
import numpy
import blend_modes

# Import background image
background_img_raw = Image.open('img/1.png')  # RGBA image

# Import foreground image
foreground_img_raw = Image.open('img/2.png')  # RGBA image
foreground_img = numpy.array(foreground_img_raw)  # Inputs to blend_modes need to be numpy arrays.
foreground_img_float = foreground_img.astype(float)  # Inputs to blend_modes need to be floats.

frame_count = 15
count  = 1
opacity = 0.0
step = 0.066
factor = 1

while count <= frame_count:
    enhancer = ImageEnhance.Contrast(background_img_raw)
    background_img_raw = enhancer.enhance(factor)
    background_img = numpy.array(background_img_raw)  # Inputs to blend_modes need to be numpy arrays.
    background_img_float = background_img.astype(float)  # Inputs to blend_modes need to be floats.

    # Blend images
    blended_img_float = blend_modes.hard_light(background_img_float, foreground_img_float, opacity)

    # Convert blended image back into PIL image
    blended_img = numpy.uint8(blended_img_float)  # Image needs to be converted back to uint8 type for PIL handling.
    blended_img_raw = Image.fromarray(blended_img)  # Note that alpha channels are displayed in black by PIL by default.
                                                    # This behavior is difficult to change (although possible).
                                                    # If you have alpha channels in your images, then you should give
                                                    # OpenCV a try.
    # Display blended image
    blended_img_raw.save(f"frames/{count}.png")
    blended_img_raw.save(f"frames/{(frame_count * 2) - (count - 1)}.png")
    opacity += step  # The opacity of the foreground that is blended onto the background is 70 %.
    factor += step * 2
    count += 1
