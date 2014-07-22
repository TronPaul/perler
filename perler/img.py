import math
import PIL.Image as Image
from enum import Enum


class Location(Enum):
    top_left = 1
    bottom_right = 2


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


def find_left_edge(row, rgb=None):
    middle = math.ceil(len(row) / 2)
    max_trans = None
    for x in range(middle, -1, -1):
        pixel = row[x]
        # Maybe contiguous transparency
        if pixel == rgb and max_trans is None:
            max_trans = x
        # Not contiguous transparency
        elif pixel != rgb and max_trans is not None:
            max_trans = None
            break
    return max_trans


def find_right_edge(row, rgb=None):
    rev_edge = find_left_edge(list(reversed(row)), rgb)
    return len(row) - rev_edge if rev_edge else None


def convert_transparent(image, location=Location.top_left):
    if location == Location.top_left:
        rgb = image.pixels[0][0]
        pixels = image.pixels
    else:
        rgb = image.pixels[-1][-1]
        pixels = [[p for p in reversed(row)] for row in reversed(image.pixels)]
    modified_pixels = []
    made_transparent = False
    for row in image:
        if any(pixel != rgb for pixel in pixels):
            # Left side
            left_edge = find_left_edge(row, rgb)
            # Right side
            right_edge = find_right_edge(row, rgb)
            modified_pixels.append([None] * left_edge + row[left_edge:right_edge] + [None] * right_edge)
        else:
            modified_pixels.append(row)
    return PerlerImage(modified_pixels, transparent=made_transparent)


def crop_transparent(image):
    img_pixels = image.pixels
    middle = math.ceil(len(img_pixels[0]) / 2)
    left_edge, right_edge, top_edge, bottom_edge = len(img_pixels[0]), 0, len(img_pixels), 0
    found_non_empty_row = False
    for y, row in enumerate(img_pixels):
        if any(pixel is not None for pixel in row):
            # Left
            max_trans = find_left_edge(row)
            if max_trans is not None:
                left_edge = min(max_trans, left_edge)
            # Right
            min_trans = find_right_edge(row)
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
    return PerlerImage(img_pixels, image.transparent)

