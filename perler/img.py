import math
from copy import deepcopy
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


def get_possible(i, boundary):
    if i == 0:
        return 0, 1
    elif i == boundary - 1:
        return i - 1, i
    else:
        return i - 1, i, i + 1


def get_adj(pos, size):
    x, y = pos
    max_x, max_y = size
    possible_x = get_possible(x, max_x)
    possible_y = get_possible(y, max_y)
    possible = set([(new_x, y) for new_x in possible_x] + [(x, new_y) for new_y in possible_y])
    possible.remove(pos)
    return list(possible)


def convert_transparent(image, location=Location.top_left):
    if location == Location.top_left:
        rgb = image.pixels[0][0]
    else:
        rgb = image.pixels[-1][-1]
    size_x, size_y = len(image.pixels[0]), len(image.pixels)
    queue = [(0, 0), (0, size_y - 1), (size_x - 1, 0), (size_x - 1, size_y - 1)]
    made_transparent = False
    modified_pixels = deepcopy(image.pixels)
    touched = set()
    while queue:
        x, y = queue.pop(0)
        if (x, y) in touched:
            continue
        touched.add((x, y))
        if modified_pixels[y][x] == rgb:
            made_transparent = True
            modified_pixels[y][x] = None
            adj = get_adj((x, y), (size_x, size_y))
            queue.extend([a for a in adj if a not in touched])
    return PerlerImage(modified_pixels, transparent=made_transparent)


def crop_transparent(image):
    img_pixels = image.pixels
    left_edge, right_edge, top_edge, bottom_edge = len(img_pixels[0]), 0, len(img_pixels), 0
    found_non_empty_row = False
    for y, row in enumerate(img_pixels):
        if any(pixel is not None for pixel in row):
            found_non_empty_row = True
            bottom_edge = y
        # advance top edge
        elif not found_non_empty_row:
            top_edge = y
    found_non_empty_column = False
    for x in range(len(img_pixels[0])):
        column = [img_pixels[y][x] for y in range(len(img_pixels))]
        if any(pixel is not None for pixel in column):
            found_non_empty_column = True
            right_edge = x
        elif not found_non_empty_column:
            left_edge = x
    if top_edge != len(img_pixels) and bottom_edge != 0:
        img_pixels = img_pixels[top_edge:bottom_edge + 1]
    if left_edge != len(img_pixels[0]) and right_edge != 0:
        img_pixels = [row[left_edge:right_edge + 1] for row in img_pixels]
    return PerlerImage(img_pixels, image.transparent)

