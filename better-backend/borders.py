from PIL import Image, ImageDraw
import math

def remove_feathering(img: Image.Image):
    new_img = Image.new("RGBA", img.size)

    for x in range(img.width):
        for y in range(img.height):
            r, g, b, a = img.getpixel((x, y))
            new_a = 0 if a < 128 else 255
            new_img.putpixel((x, y), (r, g, b, new_a))

    return new_img

def draw_border(img: Image.Image, thickness = 4):
    border_img = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(border_img)

    for x in range(img.width):
        for y in range(img.height):
            alpha = img.getpixel((x, y))[3]
            if alpha == 255:
                neighbours = [
                    (x-1, y), (x+1, y), (x, y-1), (x, y+1)
                ]

                for nx, ny in neighbours:
                    if 0 <= nx < img.width and 0 <= ny < img.height:
                        neighbout_alpha = img.getpixel((nx, ny))[3]

                        if neighbout_alpha < 255:
                            draw.ellipse((x-thickness, y-thickness, x+thickness, y+thickness), fill=(0, 0, 0, 255))
                            break

    return Image.alpha_composite(img, border_img)

def preprocess(img: Image.Image):
    img.thumbnail((512, 512))

    left = (img.width - 512) // 2
    top = (img.height - 512) // 2
    right = left + 512
    bottom = top + 512
    img = img.crop((left, top, right, bottom))

    return img

def postprocess(img: Image.Image):
    thresh = remove_feathering(img)
    borders = draw_border(thresh)
    bbox = borders.getbbox()
    scaled = scale_image(borders.crop(bbox))
    return scaled

def scale_image(img, target_size=(512, 512), background_color=(255, 255, 255, 0)):
    original_image = img

    # Calculate the scaling factor for width and height
    width_ratio = float(target_size[0] / original_image.width)
    height_ratio = float(target_size[1] / original_image.height)

    # Choose the minimum ratio to ensure that the entire image fits in the new size
    min_ratio = min(width_ratio, height_ratio)

    # Calculate the new size without distorting the aspect ratio
    new_size = (int(original_image.width * min_ratio), int(original_image.height * min_ratio))

    # Create a new image with the target size and the specified background color
    scaled_image = Image.new("RGBA", target_size, background_color)

    # Calculate the position to paste the original image without distortion
    paste_position = (
        (target_size[0] - new_size[0]) // 2,
        (target_size[1] - new_size[1]) // 2
    )

    # Paste the original image onto the new image
    scaled_image.paste(original_image.resize(new_size, Image.Resampling.LANCZOS), paste_position)

    return scaled_image

def raycast_inwards(img: Image.Image, in_angle, step_size=4):
    length = math.sqrt(2 * math.pow(img.width / 2, 2))
    dx, dy = math.cos(in_angle), math.sin(in_angle)
    x, y = length * -dx + img.width/2, length * -dy + img.height/2
    num_steps = int(length / step_size)

    for i in range(num_steps):
        ix, iy = int(x), int(y)
        if ix < 0 or ix >= img.width or iy < 0 or iy >= img.height:
            x += dx * step_size
            y += dy * step_size
            continue

        alpha = img.getpixel((ix, iy))[3]
        if alpha > 0:
            break

        x += dx * step_size
        y += dy * step_size

    return (x + dx * step_size, y + dy * step_size)
