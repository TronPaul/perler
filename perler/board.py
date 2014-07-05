import perler.bead
import functools

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
