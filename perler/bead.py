import functools
import operator


class PerlerColor(object):
    def __init__(self, code, name, rgb, type_):
        self.code = code
        self.name = name
        self.rgb = rgb
        self.type_ = type_

    @property
    def rgba(self):
        return self.rgb + (255,)

    def __repr__(self):
        return "<PerlerColor {code} ({r},{g},{b})>".format(code=self.code,
            r=self.rgb[0], g=self.rgb[1], b=self.rgb[2])


def best_match(palette, rgb):
    diff = functools.partial(diff_color, real_rgb=rgb)
    diffs_colors = [(sum(map(abs, diff(other_rgb=c.rgb))), c) for c in palette]
    return min(diffs_colors, key=operator.itemgetter(0))[1]


def diff_color(real_rgb, other_rgb):
    return tuple(a - b for (a, b) in zip(real_rgb, other_rgb))
