import perler.bead

def convert_to_perler(pixels, pallette):
    best_match = functools.partial(perler.bead, pallette)
    return [[best_match(rgb) for rgb in row] for row in pixels]
