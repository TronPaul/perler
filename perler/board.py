import perler.bead
import functools

def convert_to_perler(pixels, pallette):
    best_match = functools.partial(perler.bead.best_match, pallette)
    return [[best_match(rgb) for rgb in row] for row in pixels]
