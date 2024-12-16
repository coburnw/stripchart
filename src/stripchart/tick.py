import math

import tkinter as tk

from . import quantity


class Tick():
    def __init__(self, axis, quantity, color='black'):
        """

        :param axis: (Axis)
        :param quantity: (Quantity)
        :param color: (tk.color)
        """
        self.axis = axis
        self._quantity = quantity
        self.color = color

        self._is_major = False
        self._tick_length = 10
        self.text_offset = 15
        return

    def __repr__(self) -> str:
        return self._quantity.__repr__()

    @property
    def value(self) -> float:
        return self._quantity.value

    @property
    def is_major(self) -> bool:
        return self._is_major

    @is_major.setter
    def is_major(self, boolean):
        self._is_major = boolean
        return

    @property
    def length(self) -> float:
        if self.is_major:
            return self._tick_length
        else:
            return self._tick_length/2

    @property
    def label(self) -> str:
        printable = quantity.SI(self._quantity, precision=3)
        return '{}{}'.format(printable.coefficient, printable.exponent)

    def place_x_tick(self, chart, x0, y0):
        tick_length = self.length
        text_offset = self.text_offset

        if self.axis.position == 'top':
            tick_length = -self.length
            text_offset = -1 * self.text_offset

        if self.is_major:
            chart.create_text(x0, y0 + text_offset, anchor=tk.CENTER, text=self.label, fill=self.color)
            chart.create_line(x0, y0, x0, y0 - tick_length, fill=self.color)
        else:
            chart.create_line(x0, y0, x0, y0 - tick_length / 2, fill=self.color)

        return

    def place_y_tick(self, chart, x0, y0):

        if self.axis.position == 'left':
            tick_length = self.length
            text_offset = self.text_offset
            anchor = tk.SE
        else:
            tick_length = -self.length
            text_offset = -self.text_offset
            anchor = tk.SW

        if self.is_major:
            chart.create_text(x0 - text_offset, y0 + 10, anchor=anchor, text=self.label, fill=self.color)
            chart.create_line(x0, y0, x0 + tick_length, y0, fill=self.color)
        else:
            chart.create_line(x0, y0, x0 + tick_length / 2, y0, fill=self.color)

        return


# class Span():
#     def __init__(self, min_value, max_value):
#         pass


class TickSpan():
    def __init__(self, axis):
        self.axis = axis

        self.min_tick = None
        self.max_tick = None

        return

    def __repr__(self):
        return 'TickSpan from {} to {}'.format(self.min_tick.value, self.max_tick.value)

    @property
    def min_value(self):
        return self.min_tick.value

    @property
    def max_value(self):
        return self.max_tick.value

    @property
    def length(self):
        return self.max_tick.value - self.min_tick.value

    def set_span(self, min_val, max_val):
        """
        determines and sets a pleasing tick span given the expected min
        and max values.
        :param min_val: (float) the bottom/left most expected value
        :param max_val:  (float) the top/right most expected value
        :return: (None)
        """
        quant = quantity.Quantity(min_val)
        self.min_tick = Tick(self.axis, quant)

        quant = quantity.Quantity(max_val)
        self.max_tick = Tick(self.axis, quant)

        return

    def is_valid(self, axis, value):
        """
        Check if value is inside span
        :param axis: (Axis) the base axis
        :param value: (float) the value to place on axis
        :return: (bool) true if value is in span
        """
        if value < self.min_tick.value:
            raise ValueError('{}: {}<{}'.format(axis.name, value, self.min_tick.value))
        if value > self.max_tick.value:
            raise ValueError('{}: {}>{}'.format(axis.name, value, self.max_tick.value))

        return True


class LinTickSpan(TickSpan):
    def __init__(self, axis):
        super().__init__(axis)

        return

    def nice_number(self, value, round_=False):
        """
        Convert an input quantity into a pretty number suitable for a tick
        :param value: (float)  ugly real number
        :param round_: (bool) enable rounding
        :return: (float) rounded max/min quantity
        """
        # https://stackoverflow.com/a/4955179
        exponent = math.floor(math.log(value, 10))
        fraction = value / 10 ** exponent

        if round_:
            if fraction < 1.5:
                nice_fraction = 1.
            elif fraction < 3.:
                nice_fraction = 2.
            elif fraction < 7.:
                nice_fraction = 5.
            else:
                nice_fraction = 10.
        else:
            if fraction <= 1:
                nice_fraction = 1.
            elif fraction <= 2:
                nice_fraction = 2.
            elif fraction <= 5:
                nice_fraction = 5.
            else:
                nice_fraction = 10.

        return nice_fraction * 10 ** exponent

    def nice_bounds(self, axis_start, axis_end, num_ticks=10):
        """
        nice_bounds(axis_start, axis_end, num_ticks=10) -> tuple
        @return: (nice_axis_start, nice_axis_end, nice_tick_width)
        """
        # https://stackoverflow.com/a/4955179
        axis_width = axis_end - axis_start
        if axis_width == 0:
            nice_tick = 0
        else:
            nice_range = self.nice_number(axis_width)
            nice_tick = self.nice_number(nice_range / (num_ticks - 1), round_=True)
            axis_start = math.floor(axis_start / nice_tick) * nice_tick
            axis_end = math.ceil(axis_end / nice_tick) * nice_tick

        return axis_start, axis_end, nice_tick

    def ticks(self):
        start, stop, step = self.nice_bounds(self.min_tick.value, self.max_tick.value)
        print(start, stop, step)

        for value in range(int(start*1000), int(stop*1000), int(step*1000)):
            value = value / 1000
            tick_val = quantity.Quantity(value)
            tick = Tick(self.axis, tick_val)
            if int(value*10) % 2 == 0:
                tick.is_major = True
            yield tick

        return

    def to_coord(self, axis, value):
        """
        convert a scale value to an axis coordinate position

        :param axis: (Axis) an axis coordinate system to apply the quantity to
        :param value: (float) the value to be plotted
        :return: (float) value translated to axis coordinates
        """
        self.is_valid(axis, value)

        value = value - self.min_tick.value
        ratio = value / self.length

        coord = axis.ratio_to_coord(ratio)

        return coord


class LogTickSpan(TickSpan):
    def __init__(self, axis):
        super().__init__(axis)

        self.ticks_per_decade = 10
        return

    def logarithmic_decade(self, start, stop, numbers_per_decade):
        # https://stackoverflow.com/a/36804364
        decade_count = math.floor(math.log10(abs(stop))) - math.floor(math.log10(abs(start)))
        offset = 10 * start  # idk

        sweep_range = []
        for decade in range(0, decade_count):
            for n in range(numbers_per_decade):
                frequency = offset * 10.0 ** (n / float(numbers_per_decade))
                sweep_range.append(frequency * 10**decade)

        sweep_range.append(stop)

        return sweep_range

    def ticks(self):
        print('ticks() from {} to {}'.format(self.min_tick.value, self.max_tick.value))
        start = self.min_tick.value
        stop = self.max_tick.value

        decade_count = math.floor(math.log10(abs(stop))) - math.floor(math.log10(abs(start)))

        for decade in range(0, decade_count):
            for n in range(1, self.ticks_per_decade):
                f = n * start * 10**decade
                freq = quantity.Quantity(f, units='Hz')
                tick = Tick(self.axis, freq)
                if n in [1, 2, 5]:
                    tick.is_major = True
                yield tick

        return

    def to_coord(self, axis, value):
        """
        convert a scale quantity to an axis coordinate position

        :param axis: (Axis) an axis coordinate system to aply the quantity to
        :param value: (float) a value to be plotted
        :return: (float) a value translated to an axis coordinate
        """
        self.is_valid(axis, value)

        log_value = math.log10(value) - math.log10(self.min_tick.value)
        log_length = math.log10(self.max_tick.value) - math.log10(self.min_tick.value)

        ratio = log_value / log_length

        return axis.ratio_to_coord(ratio)
