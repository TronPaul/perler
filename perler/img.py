import math
import PIL.Image as Image


class PerlerImage:
    def __init__(self, pixels, transparent=False):
        self.pixels = pixels
        self.transparent = transparent


def read_image(image_path):
    img = Image.open(image_path)
    if img.mode != 'RGBA':
        alpha = False
        img, old = img.convert('RGBA'), img
        old.close()
        print('Warning: This image is not transparent, there may be extra unwanted pixels!')
    else:
        alpha = True
    x_size, y_size = img.size
    pixels = []
    for y in range(y_size):
        row = []
        pixels.append(row)
        for x in range(x_size):
            p = img.getpixel((x, y))
            if p[3] == 0:
                p = None
            else:
                p = p[:3]
            row.append(p)
    img.close()
    return PerlerImage(pixels, alpha)


def crop_transparent(img_pixels):
    middle = math.ceil(len(img_pixels[0]) / 2)
    left_edge, right_edge, top_edge, bottom_edge = len(img_pixels[0]), 0, len(img_pixels), 0
    found_non_empty_row = False
    for y, row in enumerate(img_pixels):
        if any(pixel is not None for pixel in row):
            # Left
            max_trans = None
            for x in range(middle, -1, -1):
                pixel = row[x]
                # Maybe contiguous transparency
                if not pixel and max_trans is None:
                    max_trans = x
                # Not contiguous transparency
                elif pixel and max_trans is not None:
                    max_trans = None
                    break
            if max_trans is not None:
                left_edge = min(max_trans, left_edge)
            # Right
            min_trans = None
            for x in range(middle, len(img_pixels[0])):
                pixel = row[x]
                # Maybe contiguous transparency
                if not pixel and min_trans is None:
                    min_trans = x
                # Not contiguous transparency
                elif pixel and min_trans is not None:
                    min_trans = None
                    break
            if min_trans is not None:
                right_edge = max(min_trans, right_edge)
            found_non_empty_row = True
            # advance bottom edge
            if found_non_empty_row:
                bottom_edge = y
        # advance top edge
        elif not found_non_empty_row:
            top_edge = y
    if top_edge != len(img_pixels) and bottom_edge != 0:
        img_pixels = img_pixels[top_edge:bottom_edge + 1]
    if left_edge != len(img_pixels[0]) and right_edge != 0:
        img_pixels = [row[left_edge:right_edge + 1] for row in img_pixels]
    return img_pixels

