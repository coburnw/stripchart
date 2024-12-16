from collections import namedtuple

Point = namedtuple('Point', 'x y')


class Axis():
    def __init__(self, chart, axis, position, title, color):
        self.chart = chart

        if axis not in ['x', 'y', 'zy']:
            raise ValueError

        self.name = axis

        self.position = position
        self.title = title
        self.color = color

        self.scales = []

        return

    # @property
    # def index(self):
    #     return self._index

    def append_scale(self, scale):
        scale.index = len(self.scales)
        self.scales.append(scale)
        return

    def place(self):
        for scale in self.scales:
            scale.place()

        return


class HorizontalAxis(Axis):
    def __init__(self, chart, position, title='', color='black'):
        if position not in ['top', 'bottom', 'center']:
            raise ValueError

        super().__init__(chart, 'x', position, title, color)

        self._margin = 100

        # Chart Canvas 0,0 is upper left corner, +x,+y = lower right corner
        # define our line segment:
        y = 0
        if self.position == 'top':
            y = self._margin
        elif self.position == 'center':
            y = self.chart.height/2
        elif self.position == 'bottom':
            y = self.chart.height - self._margin

        # x locations are the same in a vertical line
        self.x0, self.y0 = self._margin, y
        self.x1, self.y1 = self.chart.width - self._margin, y

        return

    @property
    def margin(self):
        return self._margin

    @property
    def width(self):
        return self.x1 - self.x0

    @property
    def length(self):
        return self.width

    def start_point(self, index):
        x = self.x0
        y = self.y0 + index * 50

        return Point(x=x, y=y)

    def end_point(self, index):
        x = self.x1
        y = self.y1 + index * 50

        return Point(x=x, y=y)

    def ratio_to_coord(self, ratio):
        coord = self.length * ratio

        return coord + self.margin


class VerticalAxis(Axis):
    def __init__(self, chart, position, title='', color='black'):
        if position not in ['left', 'right', 'center']:
            raise ValueError

        super().__init__(chart, 'y', position, title, color)

        self._margin = 100

        # Chart Canvas 0,0 is upper left corner, +x,+y = lower right corner
        # define our line segment:
        x = 0
        if self.position == 'left':
            x = self._margin
        elif self.position == 'center':
            x = self.chart.height/2
        elif self.position == 'right':
            x = self.chart.width - self._margin

        # x locations are the same in a vertical line
        self.x0, self.y0 = x, self._margin
        self.x1, self.y1 = x, self.chart.height - self._margin

        return

    @property
    def margin(self):
        return self._margin

    @property
    def height(self):
        return self.y1 - self.y0

    @property
    def length(self):
        return self.height

    def start_point(self, index):
        x = self.x0 + index * 50
        y = self.y0

        return Point(x=x, y=y)

    def end_point(self, index):
        x = self.x1 + index * 50
        y = self.y1

        return Point(x=x, y=y)

    def ratio_to_coord(self, ratio):
        value = self.length * ratio
        bottom = self.length + self.margin
        coord = bottom - value

        return coord
