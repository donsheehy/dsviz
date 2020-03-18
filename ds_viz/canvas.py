from ds_viz.svgengine import SVGEngine
from ds_viz.default_styles import default_styles
from ds_viz.primitives import *
from ds_viz.vector import Vector

class Canvas:
    """
    The Canvas collects geometric primitives for later output.

    It is responsible for storing and managing styles.
    Also, as styles can require multiple primitives, this mutliplication is
    performed by the Canvas.

    It is also responsible for ordering the primitives on the z-axis.
    """
    def __init__(self, width, height, styles = default_styles):
        self.width = width
        self.height = height
        self.styles = styles
        self._primitives = []

    def point(self, point, style = '_point'):
        for s in self.styles[style]:
            self._primitives.append(Circle(point, s['radius'], s))

    def line(self, a, b, style = '_line'):
        for s in self.styles[style]:
            # arrow heads?
            self._primitives.append(Line(a, b, s))

    def circle(self, center, radius, style = '_circle'):
        for s in self.styles[style]:
            # newcenter = center + s['center_offset']
            # newradius = radius + s['radius_adjust']
            # self._primitives.append(Circle(newcenter, newradius, s))
            self._primitives.append(Circle(center, radius, s))

    def rectangle(self, topleft, width, height, style = '_rectangle'):
        for s in self.styles[style]:
            a = Vector(topleft)
            b = a + Vector(width, 0)
            c = a + Vector(width, height)
            d = a + Vector(0, height)
            self._primitives.append(Polygon([a,b,c,d], s))

    def text(self, text, position, style = '_text'):
        for s in self.styles[style]:
            self._primitives.append(Text(text, position, s))

    def primitives(self):
        # Sort the primitives
        return iter(self._primitives)

    def pdfout(self, filename):
        pass

    def pngout(self, filename = None):
        pass

    def svgout(self, filename = None):
        engine = SVGEngine(self)
        # engine.draw_rect((0, 0), self.width, self.height)
        # for shape in self.shapes:
        #     shape.svg(engine)
        return str(engine)