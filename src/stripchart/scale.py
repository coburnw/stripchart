import tkinter as tk

from . import tick


class Scale():
    def __init__(self, axis, units, color):
        self.axis = axis
        self.units = units
        self.color = color

        self.index = 0

        self.left_margin = 0
        self.right_margin = 0
        self.top_margin = 0
        self.bottom_margin = 0

        self.span = None  # Log or Lin TickSpan object
        self.labels = []

        return

    def to_coord(self, value):
        return self.span.to_coord(self.axis, value)

    def place(self, chart, span_min, span_max):
        print('{}-scale place: min={}, max={}'.format(self.axis.name, span_min, span_max))
        self.span.set_span(span_min, span_max)

        start_point = self.axis.start_point(self.index)
        end_point = self.axis.end_point(self.index)

        self.place_line(chart, start_point, end_point)
        self.place_ticks(chart, start_point)
        self.place_label(chart, start_point, end_point)

        return

    def place_line(self, chart, sp, ep):
        chart.create_line(sp.x, sp.y, ep.x, ep.y, fill=self.color)
        return

    def place_label(self, chart, start_point, end_point):
        label = ''
        if len(self.labels) > 0:
            label = self.labels[0]

        text = '{} ({})'.format(label, self.units)

        if self.axis.name == 'x':
            angle = 0
            anchor = tk.CENTER

            # bottom xy position
            x = start_point.x + (end_point.x - start_point.x) / 2
            y = start_point.y + 40
            if self.axis.position == 'center':
                x = end_point.x - 20
            elif self.axis.position == 'top':
                y = (start_point.y - 40)

        else:
            angle = 90
            anchor = tk.CENTER

            x_offset = -50
            y_offset = (end_point.y-start_point.y)/2
            if self.axis.position == 'right':
                x_offset = -x_offset

            x = end_point.x + x_offset
            y = start_point.y + y_offset

        chart.create_text(x, y, anchor=anchor, angle=angle, text=text, fill=self.color)

        return

    def place_ticks(self, chart, start_point):
        print('placing ticks({}): {}'.format(self.axis.name, self.span))
        index = 0
        for tick in self.span.ticks():
            print(' tick {}'.format(tick))
            pos = self.span.to_coord(self.axis, tick.value)
            if self.axis.name == 'x':  # and index > 0:
                tick.place_x_tick(chart, pos, start_point.y)

            elif self.axis.name == 'y':
                tick.place_y_tick(chart, start_point.x, pos)

            index += 1
        return


class LinearScale(Scale):
    def __init__(self, axis, units='', color='black'):
        super().__init__(axis, units, color)

        self.span = tick.LinTickSpan(axis)

        return


class LogScale(Scale):
    def __init__(self, axis, units='', color='black'):
        super().__init__(axis, units, color)

        self.span = tick.LogTickSpan(axis)

        return

    def logarithmic_decade(self, numbers_per_decade, offset=10):
        # https://stackoverflow.com/a/36804364
        for n in range(numbers_per_decade):
            yield offset * 10.0 ** (n / float(numbers_per_decade))

        return
