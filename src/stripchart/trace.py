import collections


class Trace():
    def __init__(self, x_scale, y_scale, label=None, color=None):
        self.x_scale = x_scale
        self.y_scale = y_scale

        self.label = label
        if self.label is not None:
            self.y_scale.labels.append(self.label)

        self.color = color
        if color is None:
            self.color = y_scale.color

        self.is_empty = True
        self.x0 = None
        self.y0 = None

        self.segments = collections.deque()  # pronounced deck
        return

    @property
    def units(self):
        return self.y_scale.units

    def next_value(self):
        """
        Returns the next float value in the sequence to be plotted.
        Implemented by the application subclass.
        """
        raise NotImplemented

    def update(self, chart):
        x, y = self.next_value()
        self.append(chart, x, y)
        return
    
    def append(self, chart, x1, y1):
        xy = []

        if self.x0 is None:
            self.x0 = x1
            self.y0 = y1

        xy.append(self.x_scale.to_coord(self.x0))
        xy.append(self.y_scale.to_coord(self.y0))

        xy.append(self.x_scale.to_coord(x1))
        xy.append(self.y_scale.to_coord(y1))

        self.x0 = x1
        self.y0 = y1
        
        segment = chart.create_line(xy, fill=self.color)
        self.segments.append(segment)  # then use popleft() to delete
        
        return True

    def erase(self, chart):
        try:
            while True:
                segment = self.segments.popleft()
                chart.delete(segment)
        except IndexError:
            pass

        self.x0 = None

        return
