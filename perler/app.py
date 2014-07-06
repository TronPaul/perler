import PIL.Image as Image
import perler.board
import perler.bead
import csv
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
    board = perler.board.convert_to_perler(pixels, palette)
    board_pixels = [[c.rgb[:3] if c else None for c in row] for row in board]
    perler_pdf_path = PurePath(image_path).stem + '_perler.pdf'
    perler.board.draw_board(board_pixels, perler_pdf_path)
    perler_palette_path = PurePath(image_path).stem + '_perler_palette.csv'
    palette_used = {}
    for row in board:
        for c in row:
            if c.code in palette_used:
                palette_used[c.code] = (c, palette_used[c.code][1] + 1)
            else:
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
            p = img.getpixel((x,y))
            if p[3] == 0:
                p = None
            else:
                p = p[:3]
            row.append(p)
    img.close()
    return pixels


def read_palette(palette_path):
    palette = []
    with open(palette_path) as f:
        for i, line in enumerate(f):
            if i == 0:
                continue
            code, name, r, g, b, type_, _ = line.split(',')
            palette.append(perler.bead.PerlerColor(code,
                name, (int(r),int(g),int(b)), type_))
    return palette


def write_palette(palette, palette_path):
    with open(palette_path, 'w') as fp:
        writer = csv.writer(fp)
        writer.writerow(('Code', 'Name', 'Count'))
        for c, count in palette.values():
            writer.writerow((c.code, c.name, count))