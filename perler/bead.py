import functools
import operator

class PerlerColor(object):
    def __init__(self, code, name, rgb, type_):
        self.code = code
        self.name = name
        self.rgb = rgb
        self.type_ = type_

    def __repr__(self):
        return "<PerlerColor {code} ({r},{g},{b})>".format(code=self.code,
            r=self.rgb[0], g=self.rgb[1], b=self.rgb[2])

def best_match(pallette, rgb):
    diff = functools.partial(diff_color, rgb)
    diffs_colors = [(sum(map(abs, diff(c.rgb))), c) for c in pallette]
    return min(diffs_colors, key=operator.itemgetter(0))[1]

def diff_color(rgbA, rgbB):
    return tuple(a - b for (a, b) in zip(rgbA, rgbB))

def diff_color_normalized(rgbA, rgbB):
    return tuple((a - b) / a for (a, b) in zip(rgbA, rgbB))
