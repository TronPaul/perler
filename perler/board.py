import perler.bead
import cairo
import functools
import math

page_width = 595
page_height = 842
point_to_milimeter = 72/25.4

BEAD_RADIUS = 1.75
BEAD_THICKNESS = 1
BOARD_SPACING = 4.8
BOARD_BORDER = 4

def convert_to_perler(pixels, pallette):
    best_match = functools.partial(perler.bead.best_match, pallette)
    board = []
    for row in pixels:
        beads = []
        board.append(beads)
        for rgb in row:
            if rgb:
                beads.append(best_match(rgb))
            else:
                beads.append(None)
    return board

def draw_board(pixels, path):
    with open(path, 'wb') as fp:
        pdf = cairo.PDFSurface(fp, page_width, page_height)
        cr = cairo.Context(pdf)
        cr.save()
        cr.set_source_rgb(1, 1, 1)
        cr.paint()
        cr.restore()
        for y, row in enumerate(pixels):
            pos_y = BOARD_BORDER + (y * BOARD_SPACING)
            for x, pixel in enumerate(row):
                pos_x = BOARD_BORDER + (x * BOARD_SPACING)
                if pixel:
                    cr.save()
                    cr.set_line_width(BEAD_THICKNESS)
                    cr.arc(pos_x, pos_y, BEAD_RADIUS, 0, 2 * math.pi)
                    float_pixel = tuple(c/255 for c in pixel)
                    cr.set_source_rgb(*float_pixel)
                    cr.stroke()
                    cr.restore()
                    if sum(pixel) >= 750:
                        cr.save()
                        cr.set_line_width(.25)
                        cr.set_source_rgb(0,0,0)
                        cr.arc(pos_x, pos_y, BEAD_RADIUS + BEAD_THICKNESS/2, 0, 2 * math.pi)
                        cr.stroke()
                        cr.restore()
                        cr.save()
                        cr.set_line_width(.25)
                        cr.set_source_rgb(0,0,0)
                        cr.arc(pos_x, pos_y, BEAD_RADIUS - BEAD_THICKNESS/2, 0, 2 * math.pi)
                        cr.stroke()
                        cr.restore()
        pdf.finish()

def draw_image(board, path):
    x_size, y_size = len(board[0]), len(board)
    img = Image.new('RGBA', (x_size, y_size))
    pixels = []
    for row in board:
        for c in row:
            if c:
               pixels.append(c.rgba)
            else:
               pixels.append((0,0,0,0))
    img.putdata(pixels)
    with open(path, 'wb') as fp:
        img.save(fp)
