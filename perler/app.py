import PIL.Image as Image

import perler.board

def image_to_perler_pdf(image_path, page_size, pallette_path):
    pallette = read_pallette(pallette_path)
    pixels = read_image_pixels(image_path)
    board = perler.board.convert_to_perler(pixels, pallette)

def read_image_pixels(image_path):
    img = Image.open(image_path)
    img.convert('RGB')
    return list(im.getdata())

def read_pallette(pallette_path):
    pallette = []
    with open(pallette_path) as f:
        for i, line in enumerate(f):
            if i == 0:
                continue
            code, name, r, g, b, type_, _ = line.split(',')
            pallette.append(PerlerColor(code, name, (r,g,b), type_))
    return pallette
