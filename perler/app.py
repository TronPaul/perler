import PIL.Image as Image
import perler.board
import perler.bead
import csv
import math
from pathlib import PurePath


def image_to_perler_image(image_path, palette_path):
    palette = read_palette(palette_path)
    pixels = read_image_pixels(image_path)
    board = perler.board.convert_to_perler(pixels, palette)
    perler_image_path = image_path.split('.')[0] + '_perler.' + image_path.split('.')[1]
    perler.board.draw_image(board, perler_image_path)


def image_to_perler_pdf(image_path, palette_path):
    palette = read_palette(palette_path)
    pixels = read_image_pixels(image_path)
    pixels = crop_transparent(pixels)
    board = perler.board.convert_to_perler(pixels, palette)
    board_pixels = [[c.rgb[:3] if c else None for c in row] for row in board]
    perler_pdf_path = PurePath(image_path).stem + '_perler.pdf'
    perler.board.draw_board(board_pixels, perler_pdf_path)
    perler_palette_path = PurePath(image_path).stem + '_perler_palette.csv'
    palette_used = {}
    for row in board:
        for c in row:
            if c and c.code in palette_used:
                palette_used[c.code] = (c, palette_used[c.code][1] + 1)
            elif c:
                palette_used[c.code] = (c, 0)
    write_palette(palette_used, perler_palette_path)


def read_image_pixels(image_path):
    img = Image.open(image_path)
    if img.mode != 'RGBA':
        print('Warning: This image is not transparent, there may be extra unwanted pixels!')
        img, old = img.convert('RGBA'), img
        old.close()
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
    return pixels


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
            #Right
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
        img_pixels = img_pixels[top_edge:bottom_edge+1]
    if left_edge != len(img_pixels[0]) and right_edge != 0:
        img_pixels = [row[left_edge:right_edge+1] for row in img_pixels]
    return img_pixels


def read_palette(palette_path):
    palette = []
    with open(palette_path) as f:
        for i, line in enumerate(f):
            if i == 0:
                continue
            code, name, r, g, b, type_, _ = line.split(',')
            palette.append(perler.bead.PerlerColor(code,
                                                   name, (int(r), int(g), int(b)), type_))
    return palette


def write_palette(palette, palette_path):
    with open(palette_path, 'w') as fp:
        writer = csv.writer(fp)
        writer.writerow(('Code', 'Name', 'Count'))
        for c, count in palette.values():
            writer.writerow((c.code, c.name, count))