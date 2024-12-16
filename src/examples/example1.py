import math

import tkinter as tk

import stripchart


class SineSignal():
    def __init__(self, start_time, radian_offset=0.0, step=1.0 / 6.28):
        self.x_offset = radian_offset
        self.x = start_time
        self.step = step
        self.scale = 1
        self.y_offset = 1
        return

    @property
    def x_value(self):
        return self.x

    @property
    def y_value(self):
        y = self.scale * math.sin(self.x + self.x_offset)
        return y + self.y_offset

    def advance(self):
        self.x += self.step
        return


class SignalTrace(stripchart.Trace):
    def __init__(self, signal, x_scale, y_scale, **kwargs):
        super().__init__(x_scale, y_scale, **kwargs)
        self.signal = signal
        return

    def next_value(self):
        self.signal.advance()

        return self.signal.x_value, self.signal.y_value


if __name__ == '__main__':
    root = tk.Tk()
    root.title('TK StripChart')

    chart = stripchart.Chart(root, 1200, 600, 'white')
    time_axis = stripchart.HorizontalAxis(chart, position='bottom', title='Time')
    time_scale = stripchart.LogScale(time_axis, units='Secs')

    left_axis = stripchart.VerticalAxis(chart, position='left', title='Left')
    s21_scale = stripchart.LinearScale(left_axis, units='dBm', color='red')

    right_axis = stripchart.VerticalAxis(chart, position='right', title='Right')
    s12_scale = stripchart.LinearScale(right_axis, units='dBm', color='blue')

    start_time = 10
    v_signal = SineSignal(start_time, radian_offset=0)
    s21_trace = SignalTrace(v_signal, time_scale, s21_scale, label='S21')

    i_signal = SineSignal(start_time, radian_offset=6.28 / 4)
    s12_trace = SignalTrace(i_signal, time_scale, s12_scale, label='S12')

    chart.append_scale(time_scale, min_value=start_time, max_value=1000)
    chart.append_scale(s21_scale, min_value=-20, max_value=3)
    chart.append_scale(s12_scale, min_value=0.0, max_value=2)

    chart.append_trace(s21_trace)
    chart.append_trace(s12_trace)

    chart.update(100)
    chart.show(legend=True)

    root.mainloop()
