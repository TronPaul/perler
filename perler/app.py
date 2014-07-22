from perler.board import convert_to_perler, draw_board
from perler.bead import PerlerColor
from perler.img import crop_transparent, read_image
import csv
from pathlib import PurePath


def image_to_perler_pdf(image_path, palette_path):
    palette = read_palette(palette_path)
    perler_image = read_image(image_path)
    if perler_image.transparent:
        perler_image = crop_transparent(perler_image)
    # TODO: else crop top left color
    board = convert_to_perler(perler_image.pixels, palette)
    board_pixels = [[c.rgb[:3] if c else None for c in row] for row in board]
    perler_pdf_path = PurePath(image_path).stem + '_perler.pdf'
    draw_board(board_pixels, perler_pdf_path)
    perler_palette_path = PurePath(image_path).stem + '_perler_palette.csv'
    write_palette(board, perler_palette_path)


def read_palette(palette_path):
    palette = []
    with open(palette_path) as fp:
        reader = csv.reader(fp)
        next(reader)
        for row in reader:
            code, name, r, g, b, type_, _ = row
            palette.append(PerlerColor(code, name, (int(r), int(g), int(b)), type_))
    return palette


def write_palette(board, palette_path):
    palette = {}
    for row in board:
        for c in row:
            if c and c.code in palette:
                palette[c.code] = (c, palette[c.code][1] + 1)
            elif c:
                palette[c.code] = (c, 0)

    with open(palette_path, 'w') as fp:
        writer = csv.writer(fp)
        writer.writerow(('Code', 'Name', 'Count'))
        for c, count in palette.values():
            writer.writerow((c.code, c.name, count))