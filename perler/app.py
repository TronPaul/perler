import PIL.Image as Image

import perler.board
import perler.bead

def image_to_perler_image(image_path, pallette_path):
    pallette = read_pallette(pallette_path)
    pixels = read_image_pixels(image_path)
    board = perler.board.convert_to_perler(pixels, pallette)
    perler_image_path = image_path.split('.')[0] + '_perler.' + image_path.split('.')[1]
    make_image(perler_image_path, board)

def make_image(image_path, board):
    x_size, y_size = len(board[0]), len(board)
    img = Image.new('RGBA', (x_size, y_size))
    pixels = []
    for row in board:
        for c in row:
            if c:
               pixel = c.rgb + (255,)
               pixels.append(pixel)
            else:
               pixels.append((0,0,0,0))
    img.putdata(pixels)
    with open(image_path, 'wb') as fp:
        img.save(fp)

def read_image_pixels(image_path):
    img = Image.open(image_path)
    img.convert('RGBA')
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
    return pixels

def read_pallette(pallette_path):
    pallette = []
    with open(pallette_path) as f:
        for i, line in enumerate(f):
            if i == 0:
                continue
            code, name, r, g, b, type_, _ = line.split(',')
            pallette.append(perler.bead.PerlerColor(code,
                name, (int(r),int(g),int(b)), type_))
    return pallette
